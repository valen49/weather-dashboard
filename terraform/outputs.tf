output "ip_publica" {
  description = "IP pública de la instancia EC2"
  value       = aws_instance.pin_instance.public_ip
}

output "comando_ssh" {
  description = "Comando para conectarse por SSH"
  value       = "ssh ubuntu@${aws_instance.pin_instance.public_ip}"
}
