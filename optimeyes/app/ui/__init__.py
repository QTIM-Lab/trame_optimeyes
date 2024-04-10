from .toolbar import Toolbar
from .left_drawer import LeftDrawer
from .right_drawer import RightDrawer
from .main_content import MainContent


def reload(m=None):
    from . import toolbar, left_drawer, right_drawer, main_content

    toolbar.__loader__.exec_module(toolbar)
    left_drawer.__loader__.exec_module(left_drawer)
    right_drawer.__loader__.exec_module(right_drawer)
    main_content.__loader__.exec_module(main_content)
    if m:
        m.__loader__.exec_module(m)


__all__ = [
    "Toolbar",
    "LeftDrawer",
    "RightDrawer",
    "MainContent",
]
