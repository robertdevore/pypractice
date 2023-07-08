import argparse
import csv
import datetime
from scapy.all import sniff, wrpcap
from tqdm import tqdm

start_capture_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
csv_filename = f"packet_capture_{start_capture_time}.csv"
pcap_filename = f"packet_capture_{start_capture_time}.pcap"
captured_packets = []

# Callback function to process captured packets
def process_packet(packet):
    # Extract relevant information from the packet
    packet_data = {
        "Source IP": packet[0][1].src,
        "Destination IP": packet[0][1].dst,
        "Source Port": packet[0][2].sport,
        "Destination Port": packet[0][2].dport,
        "Protocol": packet[0][1].proto,
        "Raw Data": packet[0].payload
    }

    # Save packet data to CSV file
    save_packet_data(packet_data)

    # Add packet to captured_packets list
    captured_packets.append(packet)

# Function to save packet data to CSV file
def save_packet_data(packet_data):
    with open(csv_filename, "a", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=packet_data.keys())
        writer.writerow(packet_data)

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--time", type=int, help="Duration of the packet capture in seconds")
args = parser.parse_args()

try:
    # Start capturing network traffic
    print("Starting packet capture... Press Ctrl+C to stop.")

    if args.time:
        print("Packet capture duration:", args.time, "seconds")
        with tqdm(total=args.time, unit="s") as pbar:
            # Run the packet capture for the specified duration
            sniff(prn=process_packet, timeout=args.time, count=0, store=False, stop_filter=lambda _: pbar.update(1))
        print("\nPacket capture completed.")
    else:
        # Run the packet capture indefinitely
        sniff(prn=process_packet, store=False)

except KeyboardInterrupt:
    print("\nPacket capture stopped. Captured", len(captured_packets), "packets.")

# Save captured packets to a PCAP file
wrpcap(pcap_filename, captured_packets)
