import pika
import os
import socket
import logging
from typing import Optional, Dict, Any



class QueueSystem:
    def __init__(self, 
                 host: str = None, 
                 port: int = None, 
                 username: str = None, 
                 password: str = None, 
                 vhost: str = '/'):
        # Connection parameters with extensive fallback
        self.host = host or os.getenv('RABBITMQ_HOST', 'localhost')
        self.port = port or int(os.getenv('RABBITMQ_PORT', 5672))
        self.username = username or os.getenv('RABBITMQ_USERNAME', 'guest')
        self.password = password or os.getenv('RABBITMQ_PASSWORD', 'guest')
        self.vhost = vhost or os.getenv('RABBITMQ_VHOST', '/')
        
        # Enhanced logging
        logging.basicConfig(
            level=logging.DEBUG, 
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def diagnose_connection_issues(self) -> Dict[str, Any]:
        """
        Comprehensive connection diagnostics
        
        Returns:
            Dictionary with detailed connection diagnostic information
        """
        diagnostics = {
            'host': self.host,
            'port': self.port,
            'username': self.username,
            'vhost': self.vhost,
            'network_reachable': False,
            'socket_test': None,
            'connection_details': None
        }

        try:
            # Network socket test
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            socket_result = sock.connect_ex((self.host, self.port))
            sock.close()

            diagnostics['socket_test'] = {
                'status': 'open' if socket_result == 0 else 'closed',
                'error_code': socket_result
            }

            # Detailed connection parameters
            connection_params = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                virtual_host=self.vhost,
                credentials=pika.PlainCredentials(
                    username=self.username, 
                    password=self.password
                ),
                connection_attempts=3,
                retry_delay=5,
                socket_timeout=5
            )

            # Attempt connection
            try:
                connection = pika.BlockingConnection(connection_params)
                channel = connection.channel()
                
                diagnostics.update({
                    'network_reachable': True,
                    'connection_details': {
                        'is_open': connection.is_open,
                        'server_properties': connection.server_properties
                    }
                })
                
                channel.close()
                connection.close()
            
            except Exception as conn_error:
                diagnostics['connection_error'] = str(conn_error)

        except Exception as e:
            diagnostics['diagnostic_error'] = str(e)

        return diagnostics

    def get_connection(self) -> Optional[pika.BlockingConnection]:
        """
        Attempt to establish RabbitMQ connection with comprehensive error handling
        
        Returns:
            Established connection or None
        """
        try:
            connection_params = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                virtual_host=self.vhost,
                credentials=pika.PlainCredentials(
                    username=self.username, 
                    password=self.password
                ),
                connection_attempts=3,
                retry_delay=5,
                socket_timeout=5
            )
            
            return pika.BlockingConnection(connection_params)
        
        except Exception as e:
            self.logger.error(f"Connection failed: {e}")
            return None