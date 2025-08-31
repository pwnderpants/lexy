# Command line argument parser for Lexy

import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    # Configuration class to hold parsed arguments
    debug: bool = False
    device_index: Optional[int] = None
    model_path: str = "vosk-model-small-en-us-0.15"
    list_mics: bool = False
    show_help: bool = False


class ArgumentParser:
    # Simple command line argument parser for Lexy
    
    def __init__(self):
        self.config = Config()
    
    def show_help(self) -> None:
        # Display help message
        print("Usage: lexy.py [--debug|-d] [--large-model] [--device|-m INDEX] [--list-mics|-l]")
        print("  --debug, -d: Enable debug output")
        print("  --large-model: Use large, more accurate Vosk model (1.8GB)")
        print("  --device, -m INDEX: Use specific microphone device by index")
        print("  --list-mics, -l: List available microphones and exit")
    
    def parse_args(self, args: Optional[list[str]] = None) -> Config:
        # Parse command line arguments and return configuration
        if args is None:
            args = sys.argv[1:]
        
        i = 0
        while i < len(args):
            arg = args[i]
            
            if arg == "--debug" or arg == "-d":
                self.config.debug = True
            elif arg == "--large-model":
                self.config.model_path = "vosk-model-en-us-0.22"
            elif arg == "--help" or arg == "-h":
                self.config.show_help = True
                return self.config
            elif arg == "--list-mics" or arg == "-l":
                self.config.list_mics = True
                return self.config
            elif arg == "--device" or arg == "-m":
                if i + 1 < len(args):
                    try:
                        self.config.device_index = int(args[i + 1])
                        i += 1  # Skip the next argument
                    except ValueError:
                        if self.config.debug:
                            print("Error: Device index must be a number")
                        sys.exit(1)
                else:
                    if self.config.debug:
                        print("Error: --device requires a microphone index")
                    sys.exit(1)
            else:
                print(f"Unknown argument: {arg}")
                self.show_help()
                sys.exit(1)
            
            i += 1
        
        return self.config