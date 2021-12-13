resource "kubernetes_pod" "{{cookiecutter.netapp_name}}" {
  metadata {
    name = "{{cookiecutter.netapp_name}}"
    namespace = "evolved5g"
    labels = {
      app = "{{cookiecutter.netapp_app}}"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/dummy-netapp:latest"
      name  = "dummy-netapp"
    }
  }
}

resource "kubernetes_service" "{{cookiecutter.netapp_name}}_service" {
  metadata {
    name = "{{cookiecutter.netapp_service}}"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.{{cookiecutter.netapp_name}}.metadata.0.labels.app
    }
    port {
      port = {{cookiecutter.netapp_port}}
      target_port = {{cookiecutter.netapp_target_port}}
    }
  }
}
