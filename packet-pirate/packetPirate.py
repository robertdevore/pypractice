import argparse
import csv
import datetime
import logging
import warnings
from scapy.all import sniff, wrpcap, IP

# Configure logging
logging.basicConfig(filename="packet_capture.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Disable warning notices.
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Define packet filter parameters
suspicious_ip = "192.168.0.100" # todo update this
suspicious_ports = [21, 22, 23, 25, 53, 80, 123, 179, 443, 500, 587, 3389, 8443]
block_outside_traffic = False

# Create CSV file for captured packets
csv_filename = "packet_capture.csv"
csv_file = open(csv_filename, "a", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Timestamp", "Source IP", "Destination IP", "Source Port", "Destination Port", "Protocol"])

# Variable to store captured packets
captured_packets = []

# Packet capture callback function
def process_packet(packet):
    try:
        # Extract packet information
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        src_port = packet[IP].sport
        dst_port = packet[IP].dport
        protocol = packet[IP].proto

        # Check for suspicious activity
        if block_outside_traffic and dst_ip != suspicious_ip:
            logging.warning(f"Outside traffic blocked: {packet.summary()}")
            return

        if src_ip == suspicious_ip or dst_ip == suspicious_ip or src_port in suspicious_ports or dst_port in suspicious_ports:
            logging.warning(f"Suspicious activity detected: {packet.summary()}")

        # Write packet details to CSV file
        csv_writer.writerow([timestamp, src_ip, dst_ip, src_port, dst_port, protocol])

        # Append packet to captured_packets list
        captured_packets.append(packet)

    except Exception as e:
        logging.error(f"Error processing packet: {str(e)}")

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--local", action="store_true", help="Block outside traffic")
args = parser.parse_args()

# Set block_outside_traffic flag based on command-line argument
block_outside_traffic = args.local

try:
    # Start packet capture
    logging.info("Starting packet capture... Press Ctrl+C to stop.")
    sniff(prn=process_packet, store=False)

except KeyboardInterrupt:
    logging.info("Packet capture stopped.")

except Exception as e:
    logging.error(f"Packet capture error: {str(e)}")

finally:
    # Close CSV file
    csv_file.close()

    # Save captured packets to a PCAP file
    capture_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    pcap_filename = f"packet_capture_{capture_time}.pcap"
    wrpcap(pcap_filename, captured_packets)
