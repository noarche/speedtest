from speedtest import Speedtest
import json
import argparse
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama for cross-platform color support
init(autoreset=True)


def perform_speedtest():
    """Perform speedtest and return results."""
    try:
        # Initialize Speedtest
        st = Speedtest()
        
        print(f"{Fore.CYAN}Fetching the best server based on ping...")
        best_server = st.get_best_server()
        server_details = {
            "host": best_server['host'],
            "name": best_server['name'],
            "latency_ms": round(best_server["latency"], 2),
        }
        
        print(f"{Fore.CYAN}Best server found: {Fore.GREEN}{server_details['host']} "
              f"{Fore.CYAN}(Ping: {Fore.YELLOW}{server_details['latency_ms']} ms{Fore.CYAN})")
        
        print(f"{Fore.CYAN}Performing download test...")
        download_speed = st.download()
        
        print(f"{Fore.CYAN}Performing upload test...")
        upload_speed = st.upload()
        
        # Get current time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Compile results
        results = {
            "timestamp": current_time,
            "download_speed_mbps": round(download_speed / 1e6, 2),
            "upload_speed_mbps": round(upload_speed / 1e6, 2),
            "server_details": server_details,
        }
        
        return results
        
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}")
        return None


def save_results_to_file(results, file_path="Internet.Speed.Results.json"):
    """Append results to a JSON file."""
    try:
        with open(file_path, "a") as file:
            json.dump(results, file)
            file.write("\n")  # Ensure results are stored line by line
        print(f"{Fore.GREEN}Results saved to {file_path}")
    except Exception as e:
        print(f"{Fore.RED}Error saving results to file: {e}")


def main():
    parser = argparse.ArgumentParser(description="Run a network speed test.")
    parser.add_argument("-nolog", action="store_true", help="Disable saving results to a log file.")
    args = parser.parse_args()
    
    print(f"{Fore.BLUE}Starting speed test...")
    results = perform_speedtest()
    if results:
        print(f"\n{Fore.MAGENTA}--- Speedtest Results ---")
        for key, value in results.items():
            if key == "server_details":
                print(f"\n{Fore.YELLOW}Server Details:")
                for detail_key, detail_value in value.items():
                    detail_key_display = detail_key.replace("_", " ").capitalize()
                    print(f"{Fore.CYAN}{detail_key_display}: {Fore.GREEN}{detail_value}")
            else:
                key_display = key.replace("_", " ").capitalize()
                print(f"{Fore.YELLOW}{key_display}: {Fore.CYAN}{value}")
        
        # Save the results unless the -nolog argument is used
        if not args.nolog:
            save_results_to_file(results)


if __name__ == "__main__":
    main()
