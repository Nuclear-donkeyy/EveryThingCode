require "rails/all"

module QuickstartApp
  class Application < Rails::Application
    config.load_defaults 8.0
    config.eager_load = false
    config.hosts.clear
    config.secret_key_base = "development-secret-key-base"
    config.api_only = true
  end
end
