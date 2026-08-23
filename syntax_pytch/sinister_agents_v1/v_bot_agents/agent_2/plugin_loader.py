"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: plugin_loader.py
LAST_SYNC: 2026-08-02T01:13:33Z
[/DNA_TAG]
"""
#!/usr/bin/env python3
"""
PLUGIN LOADER - Dynamic plugin system for live coding
"""
import importlib
import os
from pathlib import Path

class PluginLoader:
    def __init__(self):
        self.plugins = {}
        self.plugins_dir = Path("./plugins")
        self.active_plugins = []
        
    def discover_plugins(self):
        """Auto-discover available plugins"""
        plugins = []
        if self.plugins_dir.exists():
            for item in self.plugins_dir.iterdir():
                if item.is_dir() and (item / "__init__.py").exists():
                    plugins.append(item.name)
        return plugins
    
    def load_plugin(self, plugin_name):
        """Load a plugin dynamically"""
        try:
            # Import the plugin module
            spec = importlib.util.spec_from_file_location(
                plugin_name, 
                self.plugins_dir / plugin_name / f"{plugin_name}.py"
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get the main plugin class (assumes class name matches directory name in PascalCase)
            class_name = ''.join([word.capitalize() for word in plugin_name.split('_')])
            plugin_class = getattr(module, class_name)
            
            # Instantiate
            plugin_instance = plugin_class()
            self.plugins[plugin_name] = plugin_instance
            self.active_plugins.append(plugin_name)
            
            print(f"🔌 Loaded plugin: {plugin_name}")
            return plugin_instance
            
        except Exception as e:
            print(f"❌ Failed to load {plugin_name}: {e}")
            return None
    
    def unload_plugin(self, plugin_name):
        """Unload a plugin"""
        if plugin_name in self.plugins:
            del self.plugins[plugin_name]
            self.active_plugins.remove(plugin_name)
            print(f"🔌 Unloaded plugin: {plugin_name}")
    
    def broadcast_event(self, event_type, data):
        """Send events to all active plugins"""
        for name, plugin in self.plugins.items():
            if hasattr(plugin, 'handle_event'):
                try:
                    plugin.handle_event(event_type, data)
                except Exception as e:
                    print(f"❌ Plugin {name} error: {e}")

# Global instance
plugin_loader = PluginLoader()
