import subprocess
import core.config as mem
def importer(file_path):
   requests = []
   
   if mem.var['mode']=='W':
    with open(file_path, 'r') as f:
        for line in f.readlines():
           if line.startswith("http") and ".js" not in line:
              requests.append(line)
        return requests
   elif mem.var['mode']=='L':
        result = subprocess.run(
            [f"cat {file_path} | grep '^http'| sort -u  | grep -v '\.js'"],
          stdout=subprocess.PIPE,  # Capture standard output
          stderr=subprocess.PIPE,  # Capture standard error
          text=True,               # Work with text data instead of binary
          shell=True               # Use shell to interpret the command
      )
        if not result.stderr:
            for line in result.stdout.splitlines():
                requests.append(line)
            return requests



