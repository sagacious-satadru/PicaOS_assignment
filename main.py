from mcp.server.fastmcp import FastMCP
import datetime
from pathlib import Path
from typing import List, Optional

mcp = FastMCP()

def write_to_file(jobs: List[str], filename: str = "job-log.txt", mode: str = "w") -> str:
    """
    Write jobs to a file.
    
    Args:
        jobs: List of job details to write
        filename: Name of the output file
        mode: File opening mode ('w' for write/overwrite, 'a' for append)
    
    Returns:
        Path to the written file
    
    Raises:
        IOError: If there's an issue writing to the file
    """
    try:
        with open(filename, mode) as file:
            file.writelines(jobs)
        return filename
    except IOError as e:
        return f"Error writing to file: {str(e)}"

def read_from_file(filename: str = "job-log.txt") -> List[str]:
    """
    Read jobs from a file.
    
    Args:
        filename: Name of the file to read from
    
    Returns:
        List of job entries read from the file
    """
    try:
        if not Path(filename).exists():
            return []
            
        with open(filename, 'r') as file:
            return file.readlines()
    except IOError as e:
        print(f"Error reading file: {str(e)}")
        return []

@mcp.tool()
def store_jobs(jobs: List[str], filename: Optional[str] = None, append: bool = False) -> str:
    """
    Stores job details in the local filesystem
    
    Args:
        jobs: A list of all the job titles that are available
        filename: Optional custom filename (defaults to job-log.txt)
        append: Whether to append to existing file instead of overwriting
    
    Returns:
        Success message with local filename on success
    """
    output_file = filename or "job-log.txt"
    mode = "a" if append else "w"
    
    result = write_to_file(jobs, output_file, mode)
    if result.startswith("Error"):
        return result
    return f"Success: All jobs are successfully written to local file: {result}"

@mcp.tool()
def structure_jobs(jobs: List[str], add_timestamp: bool = False) -> List[str]:
    """
    Structures job details and returns it so that it can be stored in notion properly
    
    Args:
        jobs: A list of all the job titles that are available
        add_timestamp: Whether to add a timestamp to each job entry
    
    Returns:
        A new list where every item is a string that is formatted
    """
    formatted_jobs = []
    timestamp = f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " if add_timestamp else ""
    
    for index, job in enumerate(jobs, 1):
        formatted_job = f"{index}. {timestamp}{job.strip()}\n"
        formatted_jobs.append(formatted_job)
    
    return formatted_jobs

@mcp.tool()
def get_saved_jobs(filename: Optional[str] = None) -> List[str]:
    """
    Retrieves previously saved job details from file
    
    Args:
        filename: Optional custom filename to read from
    
    Returns:
        List of job entries previously saved
    """
    return read_from_file(filename or "job-log.txt")

if __name__ == '__main__':
    mcp.run(transport="stdio")
