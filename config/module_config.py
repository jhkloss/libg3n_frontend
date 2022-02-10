from libg3n.modules.java.java_library import JavaLibrary
from libg3n.modules.python.python_library import PythonLibrary

from libg3n.modules.java.java_config import JavaConfig
from libg3n.modules.python.python_config import PythonConfig


MODULE_CONFIG = {
    'java': JavaLibrary,
    'python': PythonLibrary
}

CONFIG_CLASSES = {
    'java': JavaConfig,
    'python': PythonConfig
}