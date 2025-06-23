#!/bin/bash

echo "🚀 Daily IT News Scheduler started"
echo "=================================="
echo "Will run daily at 07:00"
echo "Timezone: $TZ"
echo ""

# Function to run the daily task
run_daily_task() {
    echo "$(date): Starting daily IT news task..."
    
    # Run Python script directly (much simpler!)
    cd /app && python app/main.py
    
    if [ $? -eq 0 ]; then
        echo "$(date): Daily task completed successfully"
    else
        echo "$(date): Daily task failed"
    fi
}

# Function to wait until next 07:00
wait_until_07_00() {
    local now=$(date +%s)
    local target=$(date -d "07:00" +%s 2>/dev/null || date -j -f "%H:%M" "07:00" +%s 2>/dev/null)
    
    # If date command failed, use a simpler approach
    if [ -z "$target" ]; then
        local current_hour=$(date +%H)
        local current_minute=$(date +%M)
        local current_seconds=$((current_hour * 3600 + current_minute * 60))
        local target_seconds=$((7 * 3600))  # 07:00
        
        if [ $current_seconds -gt $target_seconds ]; then
            # It's past 07:00, wait until tomorrow
            target_seconds=$((target_seconds + 86400))
        fi
        
        local wait_seconds=$((target_seconds - current_seconds))
        echo "Waiting $wait_seconds seconds until next run..."
        sleep $wait_seconds
        return
    fi
    
    # If it's past 07:00 today, wait until tomorrow
    if [ $now -gt $target ]; then
        target=$(date -d "tomorrow 07:00" +%s 2>/dev/null || date -v+1d -j -f "%H:%M" "07:00" +%s 2>/dev/null)
    fi
    
    local wait_seconds=$((target - now))
    echo "Waiting $wait_seconds seconds until next run..."
    sleep $wait_seconds
}

# Main loop
while true; do
    # Wait until 07:00
    wait_until_07_00
    
    # Run the task
    run_daily_task
    
    # Wait 24 hours before next check
    echo "Waiting 24 hours until next run..."
    sleep 86400
done 