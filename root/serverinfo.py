SERVER_NAME			= "METGUIDE"
SERVER_NAME_TEST	= "DEV"
SERVER_IP			= "192.168.0.38"
SERVER_IP_TEST		= "192.168.0.38"
CH1_NAME			= "CH-1"
CH2_NAME			= "CH-2"
CH3_NAME			= "CH-3"
CH4_NAME			= "CH-4"
PORT_1				= 13000
PORT_2				= 13010
PORT_3				= 13020
PORT_4				= 13030
PORT_AUTH			= 11000
PORT_MARK			= 13000

STATE_NONE = "|cffffff00|H|h�n Lucru"

STATE_DICT = {
	0 : "....",
	1 : "|cff20c000|hRecomandat",
	2 : "BUSY",
	3 : "FULL"
}

SERVER01_CHANNEL_DICT = {
	1:{"key":11,"name":CH1_NAME,"ip":SERVER_IP,"tcp_port":PORT_1,"udp_port":PORT_1,"state":STATE_NONE,},
	2:{"key":12,"name":CH2_NAME,"ip":SERVER_IP,"tcp_port":PORT_2,"udp_port":PORT_2,"state":STATE_NONE,},
	3:{"key":13,"name":CH3_NAME,"ip":SERVER_IP,"tcp_port":PORT_3,"udp_port":PORT_3,"state":STATE_NONE,},
	4:{"key":14,"name":CH4_NAME,"ip":SERVER_IP,"tcp_port":PORT_4,"udp_port":PORT_4,"state":STATE_NONE,},
}

SERVER02_CHANNEL_DICT = {
	1:{"key":21,"name":CH1_NAME,"ip":SERVER_IP_TEST,"tcp_port":PORT_1,"udp_port":PORT_1,"state":STATE_NONE,},
	2:{"key":22,"name":CH2_NAME,"ip":SERVER_IP_TEST,"tcp_port":PORT_2,"udp_port":PORT_2,"state":STATE_NONE,},
}

REGION_NAME_DICT = {
	0 : "",		
}

REGION_AUTH_SERVER_DICT = {
	0 : {
		1 : { "ip":SERVER_IP, "port":PORT_AUTH, },
		2 : { "ip":SERVER_IP_TEST, "port":PORT_AUTH, },

	}		
}

REGION_DICT = {
	0 : {
		1 : { "name" :SERVER_NAME, "channel" : SERVER01_CHANNEL_DICT, },						
		2 : { "name" :SERVER_NAME_TEST, "channel" : SERVER02_CHANNEL_DICT, },						
	},
}

MARKADDR_DICT = {
	10 : { "ip" : SERVER_IP, "tcp_port" : PORT_MARK, "mark" : "10.tga", "symbol_path" : "10", },
	20 : { "ip" : SERVER_IP_TEST, "tcp_port" : PORT_MARK, "mark" : "20.tga", "symbol_path" : "20", },
}