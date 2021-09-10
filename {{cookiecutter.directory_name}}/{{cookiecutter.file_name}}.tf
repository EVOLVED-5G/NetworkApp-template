resource "kubernetes_pod" "dummy_netapp" {
  metadata {
    name = "{{cookiecutter.netapp_name}}"
    namespace = "{{cookicutter.netapp_namespace}}"
    labels = {
      app = "{{cookiecutter.netapp_app}}"
    }
  }

  spec {
    container {
      image = "{{cookicutter.netapp_container_image}}"
      name  = "{{cookicutter.netapp_container_name}}"
    }
  }
}

resource "kubernetes_service" "dummy_netapp_service" {
  metadata {
    name = "{{cookicutter.netapp_service}}"
    namespace = "{{cookiecutter.netapp_namespace}}"
  }
  spec {
    selector = {
      app = {{cookicutter.netapp_service_app}}
    }
    port {
      port = {{cookicutter.netapp_port}}
      target_port = {{cookiecutter.netapp_target_port}}
    }
  }
}
