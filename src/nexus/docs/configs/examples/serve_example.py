# Example: Using the hybrid configuration system in a serve command

from nexus.core.hybrid_config import get_config, is_development, get_server_config

def start_server():
    """Start server using hybrid configuration."""
    config = get_config()
    server_config = get_server_config()
    
    # Configuration-driven server setup
    host = server_config.get('host', 'localhost')
    port = server_config.get('port', 8000)
    debug = config.get('features.debug_mode', False)
    auto_reload = config.get('features.auto_reload', False)
    
    print(f"Starting server on {host}:{port}")
    print(f"Environment: {config.get('environment', 'unknown')}")
    print(f"Debug mode: {debug}")
    
    if is_development():
        print("Development mode features enabled")
        if auto_reload:
            print("Auto-reload enabled")
    
    # Start server with config settings
    # server.run(host=host, port=port, debug=debug, reload=auto_reload)
    print(f"Server would start with: host={host}, port={port}, debug={debug}, reload={auto_reload}")

if __name__ == "__main__":
    start_server()
