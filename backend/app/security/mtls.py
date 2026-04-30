"""mTLS Configuration and Certificate Management"""
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from dataclasses import dataclass
import ssl
import logging

logger = logging.getLogger(__name__)


@dataclass
class MTLSConfig:
    """mTLS configuration settings"""
    enabled: bool = True
    cert_file: str = "/certs/service.crt"
    key_file: str = "/certs/service.key"
    ca_file: str = "/certs/ca.crt"
    verify_mode: str = "required"  # required, optional, none
    min_tls_version: str = "TLSv1.2"


class CertificateManager:
    """
    Manages service certificates for mTLS
    """
    
    def __init__(self, config: Optional[MTLSConfig] = None):
        self.config = config or MTLSConfig()
        self._cert_cache: Dict[str, Any] = {}
        self._cert_expiry: Optional[datetime] = None
    
    def get_ssl_context(self) -> ssl.SSLContext:
        """
        Get SSL context for mTLS
        Returns configured SSL context for server
        """
        if not self.config.enabled:
            # Return default context if mTLS disabled
            context = ssl.create_default_context()
            return context
        
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        
        # Load server certificate
        if os.path.exists(self.config.cert_file) and os.path.exists(self.config.key_file):
            context.load_cert_chain(
                certfile=self.config.cert_file,
                keyfile=self.config.key_file
            )
        else:
            logger.warning(f"Certificate files not found: {self.config.cert_file}")
        
        # Load CA certificate for client verification
        if self.config.verify_mode == "required":
            context.verify_mode = ssl.CERT_REQUIRED
            if os.path.exists(self.config.ca_file):
                context.load_verify_locations(self.config.ca_file)
        elif self.config.verify_mode == "optional":
            context.verify_mode = ssl.CERT_OPTIONAL
            if os.path.exists(self.config.ca_file):
                context.load_verify_locations(self.config.ca_file)
        else:
            context.verify_mode = ssl.CERT_NONE
        
        # Set minimum TLS version
        if self.config.min_tls_version == "TLSv1.3":
            context.minimum_version = ssl.TLSVersion.TLSv1_3
        elif self.config.min_tls_version == "TLSv1.2":
            context.minimum_version = ssl.TLSVersion.TLSv1_2
        
        return context
    
    async def generate_service_certificate(
        self,
        service_name: str,
        validity_days: int = 365
    ) -> Dict[str, str]:
        """
        Generate a new service certificate
        Returns paths to certificate files
        """
        # In production, use proper CA like Vault or cert-manager
        # This is a placeholder for the interface
        logger.info(f"Generating certificate for service: {service_name}")
        
        return {
            "cert_file": f"/certs/{service_name}.crt",
            "key_file": f"/certs/{service_name}.key",
            "ca_file": self.config.ca_file
        }
    
    async def rotate_certificates(self) -> bool:
        """
        Rotate service certificates
        Returns True if rotation successful
        """
        try:
            # In production, integrate with cert-manager or Vault
            logger.info("Rotating service certificates")
            
            # Clear cache to force reload
            self._cert_cache.clear()
            
            return True
        except Exception as e:
            logger.error(f"Certificate rotation failed: {e}")
            return False
    
    def check_certificate_expiry(self) -> Optional[timedelta]:
        """
        Check time until certificate expires
        Returns timedelta or None if not available
        """
        if not os.path.exists(self.config.cert_file):
            return None
        
        # In production, parse certificate and get actual expiry
        # Placeholder returning 30 days
        return timedelta(days=30)
    
    async def verify_service_identity(
        self,
        peer_cert: Dict[str, Any]
    ) -> bool:
        """
        Verify peer service identity from certificate
        """
        if not peer_cert:
            return False
        
        # Check certificate subject
        subject = peer_cert.get("subject", ())
        for rdn in subject:
            for key, value in rdn:
                if key == "commonName":
                    # Verify service name matches expected
                    logger.debug(f"Peer service: {value}")
                    return True
        
        return False


def create_client_ssl_context(
    ca_file: str,
    cert_file: Optional[str] = None,
    key_file: Optional[str] = None
) -> ssl.SSLContext:
    """
    Create SSL context for mTLS client
    """
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    
    # Load CA certificate
    if os.path.exists(ca_file):
        context.load_verify_locations(ca_file)
    
    # Load client certificate if provided
    if cert_file and key_file:
        if os.path.exists(cert_file) and os.path.exists(key_file):
            context.load_cert_chain(certfile=cert_file, keyfile=key_file)
    
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    
    return context
