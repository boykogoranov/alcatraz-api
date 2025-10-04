resource "tls_private_key" "ssl_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "tls_self_signed_cert" "ssl_cert" {
  private_key_pem = tls_private_key.ssl_key.private_key_pem

  subject {
    common_name  = "alcatraz.com"
    organization = "Alcatraz"
  }

  validity_period_hours = 8760

  allowed_uses = [
    "key_encipherment",
    "digital_signature",
    "server_auth",
  ]

  dns_names    = ["alcatraz.com"]
  ip_addresses = []
}

resource "docker_secret" "ssl_cert" {
  name = "ping_api_ssl_cert_v1"
  data = base64encode(tls_self_signed_cert.ssl_cert.cert_pem)
}

resource "docker_secret" "ssl_key" {
  name = "ping_api_ssl_key_v1"
  data = base64encode(tls_private_key.ssl_key.private_key_pem)
}

resource "docker_service" "ping_api_service" {
  name = "ping-api-service"

  task_spec {
    container_spec {
      image = "ghcr.io/boykogoranov/ping-api:latest"
      
      secrets {
        secret_id   = docker_secret.ssl_cert.id
        secret_name = docker_secret.ssl_cert.name
        file_name   = "ssl_cert"
        file_uid    = "0"
        file_gid    = "0"
        file_mode   = 0444
      }
      
      secrets {
        secret_id   = docker_secret.ssl_key.id
        secret_name = docker_secret.ssl_key.name
        file_name   = "ssl_key"
        file_uid    = "0"
        file_gid    = "0"
        file_mode   = 0400
      }
    }
    
    restart_policy {
      condition    = "on-failure"
      max_attempts = 3
    }
  }

  mode {
    replicated {
      replicas = var.replicas
    }
  }

  endpoint_spec {
    ports {
      protocol       = "tcp"
      target_port    = 5000
      published_port = 5000
    }
  }

  depends_on = [
    docker_secret.ssl_cert,
    docker_secret.ssl_key
  ]
}