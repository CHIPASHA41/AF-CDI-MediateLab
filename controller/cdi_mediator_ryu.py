from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ether_types, ipv4, tcp


class CDIMediator(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    BLOCKED_WRITE_FC = {5, 6, 15, 16, 22, 43}
    ALLOWED_READ_FC = {1, 3}

    def __init__(self, *args, **kwargs):
        super(CDIMediator, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        dp = ev.msg.datapath
        parser = dp.ofproto_parser
        ofp = dp.ofproto

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofp.OFPP_CONTROLLER, ofp.OFPCML_NO_BUFFER)]
        inst = [parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]

        mod = parser.OFPFlowMod(datapath=dp, priority=0, match=match, instructions=inst)
        dp.send_msg(mod)

        self.logger.info("CDI mediation controller loaded: per-packet inspection enabled.")

    def parse_modbus_fc(self, raw_payload):
        if raw_payload is None or len(raw_payload) < 8:
            return None
        return raw_payload[7]

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath
        parser = dp.ofproto_parser
        ofp = dp.ofproto
        dpid = dp.id

        self.mac_to_port.setdefault(dpid, {})

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        if eth is None or eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return

        src = eth.src
        dst = eth.dst
        in_port = msg.match["in_port"]

        self.mac_to_port[dpid][src] = in_port

        ip_pkt = pkt.get_protocol(ipv4.ipv4)
        tcp_pkt = pkt.get_protocol(tcp.tcp)

        if ip_pkt and tcp_pkt and tcp_pkt.dst_port == 502:
            raw_payload = None
            for proto in pkt.protocols:
                if isinstance(proto, (bytes, bytearray)):
                    raw_payload = bytes(proto)
                    break

            fc = self.parse_modbus_fc(raw_payload)

            if fc in self.BLOCKED_WRITE_FC:
                self.logger.warning("BLOCKED Modbus FC=%s from %s to %s", fc, ip_pkt.src, ip_pkt.dst)
                return

            if fc in self.ALLOWED_READ_FC:
                self.logger.info("ALLOWED Modbus read FC=%s from %s to %s", fc, ip_pkt.src, ip_pkt.dst)

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofp.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        out = parser.OFPPacketOut(
            datapath=dp,
            buffer_id=ofp.OFP_NO_BUFFER,
            in_port=in_port,
            actions=actions,
            data=msg.data
        )
        dp.send_msg(out)
