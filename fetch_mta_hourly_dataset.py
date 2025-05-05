import requests
import pandas as pd
import time
import os
from datetime import datetime
from tqdm import tqdm

def download_mta_ridership_data(debug=True, total_rows=110696365, request_timeout=60):
    # API endpoint
    base_url = "https://data.ny.gov/resource/wujg-7c2s.json"
    
    # Create a directory for the data if it doesn't exist
    output_dir = "mta_ridership_data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Set batch size - maximum allowed is 50,000 for SODA 2.0 APIs
    batch_size = 45000
    
    # Keep track of total records
    total_records = 0
    
    # Counter for chunks saved to disk
    chunk_counter = 0
    
    # Keep track of failed requests
    failed_offsets = []
    
    # Set a limit for debug mode
    debug_limit = 3 * batch_size  # 3 pages
    
    # Adjust total rows for debug mode
    if debug:
        estimated_total = min(debug_limit, total_rows)
    else:
        estimated_total = total_rows
    
    # Timestamp for the file names
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print(f"Starting download at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create progress bar for the overall process
    progress_bar = tqdm(total=estimated_total, unit='records', desc="Overall Progress", position=0)
    
    # Loop until we've processed all records or hit debug limit
    offset = 0
    more_data = True
    
    while more_data:
        # Construct the API URL with limit and offset
        params = {
            "$limit": batch_size,
            "$offset": offset,
            "$order": ":id"
        }
        
        # Print status update
        tqdm.write(f"Requesting records {offset} to {offset + batch_size}...")
        
        try:
            # Make the API request with timeout
            start_time = time.time()
            response = requests.get(base_url, params=params, timeout=request_timeout)
            elapsed_time = time.time() - start_time
            
            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()
                
                # Check if we got any data
                if len(data) == 0:
                    tqdm.write("No more data available.")
                    more_data = False
                    break
                
                # Convert to DataFrame
                df = pd.DataFrame(data)
                
                # Save this batch to a CSV file
                chunk_counter += 1
                filename = f"{output_dir}/mta_ridership_{timestamp}_chunk{chunk_counter}.csv"
                df.to_csv(filename, index=False)
                
                # Update counters
                records_in_batch = len(df)
                total_records += records_in_batch
                
                # Update progress bar
                progress_bar.update(records_in_batch)
                
                # Update the description with percentage
                progress_percent = min(100, round(total_records / estimated_total * 100, 1))
                progress_bar.set_description(f"Overall Progress ({progress_percent}%)")
                
                tqdm.write(f"Saved {records_in_batch} records to {filename}")
                tqdm.write(f"Request took {elapsed_time:.2f} seconds")
                
                # Update offset for next batch
                offset += batch_size
                
                # Check if we've reached the debug limit
                if debug and total_records >= debug_limit:
                    tqdm.write(f"Debug mode: Stopping after {total_records} records")
                    more_data = False
                    break
                
                # Check if we got fewer records than requested (last batch)
                if records_in_batch < batch_size:
                    tqdm.write("Reached last batch of data.")
                    more_data = False
                    break
                
                # Small delay to avoid overloading the API
                time.sleep(1)
                
            else:
                tqdm.write(f"Error: API request failed with status code {response.status_code}")
                tqdm.write(f"Response: {response.text}")
                # Record the failed offset for later retry
                failed_offsets.append(offset)
                # Continue with the next batch instead of exiting
                offset += batch_size
                
        except requests.Timeout:
            tqdm.write(f"Request timed out after {request_timeout} seconds")
            # Record the failed offset for later retry
            failed_offsets.append(offset)
            # Continue with the next batch instead of exiting
            offset += batch_size
                
        except Exception as e:
            tqdm.write(f"An error occurred: {e}")
            # Record the failed offset for later retry
            failed_offsets.append(offset)
            # Continue with the next batch instead of exiting
            offset += batch_size
    
    # Close the progress bar
    progress_bar.close()
    
    # Report on failed requests
    if failed_offsets:
        print(f"\n{len(failed_offsets)} requests failed:")
        for failed_offset in failed_offsets:
            print(f"  - Offset {failed_offset} to {failed_offset + batch_size}")
        
        # Save failed offsets to a file for potential retry later
        with open(f"{output_dir}/failed_offsets_{timestamp}.txt", "w") as f:
            for offset in failed_offsets:
                f.write(f"{offset}\n")
        print(f"Failed offsets saved to {output_dir}/failed_offsets_{timestamp}.txt")
    
    # If we have multiple chunks, combine them into a single file
    if chunk_counter > 0:
        print(f"Download complete. Total records: {total_records}")
        
        if not debug and chunk_counter > 1:
            print(f"Combining {chunk_counter} chunks into a single file...")
            
            # Create a progress bar for the combining process
            combine_progress = tqdm(total=chunk_counter, unit='chunks', 
                                    desc="Combining Files")
            
            # Combine all chunks into a single DataFrame
            combined_df = pd.DataFrame()
            for i in range(1, chunk_counter + 1):
                chunk_file = f"{output_dir}/mta_ridership_{timestamp}_chunk{i}.csv"
                if os.path.exists(chunk_file):  # Check if file exists
                    chunk_df = pd.read_csv(chunk_file)
                    combined_df = pd.concat([combined_df, chunk_df], ignore_index=True)
                combine_progress.update(1)
            
            combine_progress.close()
            
            # Save the combined data
            print("Saving combined file...")
            combined_file = f"{output_dir}/mta_ridership_{timestamp}_complete.csv"
            combined_df.to_csv(combined_file, index=False)
            
            print(f"Combined file saved to {combined_file}")
            
            # Optionally remove the individual chunk files
            if not debug:
                print("Removing individual chunk files...")
                delete_progress = tqdm(total=chunk_counter, unit='files', desc="Deleting Chunks")
                
                for i in range(1, chunk_counter + 1):
                    chunk_file = f"{output_dir}/mta_ridership_{timestamp}_chunk{i}.csv"
                    if os.path.exists(chunk_file):  # Check if file exists
                        os.remove(chunk_file)
                    delete_progress.update(1)
                
                delete_progress.close()
        
        print(f"Finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if failed_offsets:
            print(f"Note: {len(failed_offsets)} requests failed. Some data may be missing.")

if __name__ == "__main__":
    # Set debug to False to download the entire dataset
    debug_mode = False
    
    # Total number of rows in the dataset
    total_rows = 110696365
    
    # Maximum time to wait for a request (in seconds)
    timeout = 60  # 1 minute
    
    print("MTA Subway Hourly Ridership Data Downloader")
    print(f"Debug mode: {'ON' if debug_mode else 'OFF'}")
    print(f"Total records in dataset: {total_rows:,}")
    print(f"Request timeout: {timeout} seconds")
    
    download_mta_ridership_data(debug=debug_mode, total_rows=total_rows, request_timeout=timeout)