resource "kubernetes_pod" "dummy_netapp" {
  metadata {
    name = "{{cookiecutter.netapp_name}}"
    namespace = "{{cookiecutter.netapp_namespace}}"
    labels = {
      app = "{{cookiecutter.netapp_app}}"
    }
  }

  spec {
    container {
      image = "{{cookiecutter.netapp_container_image}}"
      name  = "{{cookiecutter.netapp_container_name}}"
    }
  }
}

resource "kubernetes_service" "dummy_netapp_service" {
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
