import machine
import network
from neopixel import NeoPixel


# Parameters
NETWORK_PREFIX = "find_my_py_"
MEASURE_AVG = 3
MEASURE_THRESHOLD = -40
NEOPIXEL_PIN = 5


# Initialize NeoPixel
np = NeoPixel(machine.Pin(NEOPIXEL_PIN), 1)

# Setup Passive WiFi Network
u_id = machine.unique_id()
essid = NETWORK_PREFIX + str(int.from_bytes(u_id))

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=essid, channel=11)

print('Opened Network "{}"" on channel {}'.format(
    ap.config('essid'), ap.config('channel')))

# Setup WiFi for Search
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

print("sta_if.active: " + str(sta_if.active()))
print("ap.active: " + str(ap.active()))


def find_nodes(active_node=None):
    '''Return strongest or updated node'''

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


def set_neopixel(np, color):
    '''Write color to NeoPixel node'''
    np[0] = color
    np.write()


# Continuous Search
active_node = None
signal_strength = None

while(True):
    active_node = find_nodes(active_node)

    if active_node:
        if not signal_strength:
            signal_strength = MEASURE_AVG * [active_node[3]]
        else:
            signal_strength[1:] = signal_strength[:-1]
            signal_strength[0] = active_node[3]

        if signal_strength[0] >= MEASURE_THRESHOLD:
            print('Partner node found :)')

            # Set green LED
            set_neopixel(np, (0, 255, 0))

        else:
            prev_signal_strength = (sum(signal_strength[1:]) /
                                    (len(signal_strength) - 1))
            d_signal_strength = signal_strength[0] - prev_signal_strength
            getting_closer = (d_signal_strength > 0)

            if getting_closer:
                # Set red LED
                set_neopixel(np, (255, 0, 0))
            else:
                # Set blue LED
                set_neopixel(np, (0, 0, 255))

            print(d_signal_strength)

    else:
        signal_strength = None
        print('No node found :(')

        # Set yellow LED
        set_neopixel(np, (255, 255, 0))
