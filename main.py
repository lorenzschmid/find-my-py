import machine
import network


NETWORK_PREFIX = "find_my_py_"
MES_AVG = 3
MES_THRESHOLD = -40

# Setup Passive Network
u_id = machine.unique_id()
essid = NETWORK_PREFIX + str(u_id[0]+u_id[1]+100*(u_id[2]+u_id[3]))

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=essid, channel=11)

print('Opened Network "{}"" on channel {}'.format(
    ap.config('essid'), ap.config('channel')))

# Setup Active Network
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

print("sta_if.active: " + str(sta_if.active()))
print("ap.active: " + str(ap.active()))


def find_nodes(active_node=None):
    # Find all find-my-py nodes
    networks = sta_if.scan()
    fmp_nodes = list(
        filter(lambda x: x[0].startswith(NETWORK_PREFIX), networks))

    # Sort by signal state
    if len(fmp_nodes) == 0:
        active_node = None
    else:
        fmp_nodes.sort(key=lambda n: n[3], reverse=True)

        if active_node:
            active_node = \
                [node for node in fmp_nodes if node[0] == active_node[0]][0]
        else:
            active_node = fmp_nodes[0]

    return active_node


# Continous Search
active_node = None
signal_strength = None

while(True):
    active_node = find_nodes(active_node)

    if active_node:
        if not signal_strength:
            signal_strength = MES_AVG * [active_node[3]]
        else:
            signal_strength[1:] = signal_strength[:-1]
            signal_strength[0] = active_node[3]

        if signal_strength[0] >= MES_THRESHOLD:
            print('Partner node found :)')
            # TODO: green LED

        else:
            prev_signal_strength = (sum(signal_strength[1:]) /
                                    (len(signal_strength) - 1))
            d_signal_strength = signal_strength[0] - prev_signal_strength
            getting_closer = (d_signal_strength > 0)

            if getting_closer:
                # TODO: red LED
                pass
            else:
                # TODO: blue LED
                pass

            print(d_signal_strength)

    else:
        signal_strength = None
        print('No node found :(')

        # TODO: yellow LED
