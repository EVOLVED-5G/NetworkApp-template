resource "kubernetes_pod" "{{cookiecutter.netapp_name}}" {
  metadata {
    name = "{{cookiecutter.netapp_name}}"
    namespace = "{{cookiecutter.netapp_namespace}}"
    labels = {
      app = "{{cookiecutter.netapp_app}}"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/{{cookiecutter.netapp_name}}:latest"
      name  = "{{cookiecutter.netapp_container_name}}"
    }
  }
}

resource "kubernetes_service" "{{cookiecutter.netapp_name}}_service" {
  metadata {
    name = "{{cookiecutter.netapp_service}}"
    namespace = "{{cookiecutter.netapp_namespace}}"
  }
  spec {
    selector = {
      app = {{cookiecutter.netapp_service_app}}
    }
    port {
      port = {{cookiecutter.netapp_port}}
      target_port = {{cookiecutter.netapp_target_port}}
    }
  }
}
