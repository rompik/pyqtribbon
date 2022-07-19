import typing

from PyQt5 import QtWidgets, QtCore, QtGui

from .category import Category, CategoryStyle


class Ribbon(QtWidgets.QWidget):
    #: The categories of the ribbon.
    _categories: typing.List[Category]
    #: height of the ribbon
    _ribbonHeight: int

    #: Signal: The help button was clicked.
    helpButtonClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._categories = []
        self._ribbonHeight = 270
        self.setFixedHeight(self._ribbonHeight)

        # Tab bar layout
        self._tabsWidget = QtWidgets.QWidget(self)
        self._tabsLayout = QtWidgets.QHBoxLayout(self)
        self._tabsLayout.setContentsMargins(0, 0, 0, 0)
        self._tabsLayout.setSpacing(0)
        self._tabsWidget.setLayout(self._tabsLayout)

        # Application
        self._applicationButton = QtWidgets.QToolButton()
        self._applicationButton.setIcon(QtGui.QIcon('icons/python.png'))
        self._applicationButton.setIconSize(QtCore.QSize(32, 32))
        self._applicationButton.setText("File")
        self._applicationButton.setStyleSheet(
            "QToolButton { border: none; padding: 0px; } "
            "QToolButton::menu-indicator { image: none; } "
        )

        self._applicationButton.setToolTip("File")
        self._tabsLayout.addWidget(self._applicationButton)

        self._fileMenu = QtWidgets.QMenu(self)
        self._applicationButton.setMenu(self._fileMenu)

        # Title bar actions
        self._titleBarActions = QtWidgets.QToolBar()
        self._titleBarActions.setOrientation(QtCore.Qt.Horizontal)
        self._titleBarActions.setIconSize(QtCore.QSize(32, 32))
        self._titleBarActions.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self._tabsLayout.addWidget(self._titleBarActions)

        # tab bar
        self._tabBar = QtWidgets.QTabBar(self)
        font = self._tabBar.font()
        font.setPointSize(10)
        self._tabBar.setFont(font)
        self._tabBar.setShape(QtWidgets.QTabBar.RoundedNorth)
        self._tabBar.setDocumentMode(True)

        # min/max/close buttons
        self._rightButtonGroup = QtWidgets.QWidget()
        self._rightButtonLayout = QtWidgets.QHBoxLayout(self._rightButtonGroup)
        self._rightButtonLayout.setContentsMargins(0, 0, 0, 0)
        self._rightButtonLayout.setSpacing(5)
        self._minRibbonButton = QtWidgets.QToolButton(self)
        self._minRibbonButton.setIconSize(QtCore.QSize(32, 32))
        self._minRibbonButton.setIcon(QtGui.QIcon('icons/collapse-arrow.png'))
        self._minRibbonButton.setAutoRaise(True)
        self._minRibbonButton.setToolTip("Collapse Ribbon")
        self._helpButton = QtWidgets.QToolButton(self)
        self._helpButton.setIconSize(QtCore.QSize(32, 32))
        self._helpButton.setIcon(QtGui.QIcon("icons/help.png"))
        self._helpButton.setAutoRaise(True)
        self._helpButton.setToolTip("Help")
        self._helpButton.clicked.connect(self.helpButtonClicked)
        self._rightButtonLayout.addWidget(self._minRibbonButton)
        self._rightButtonLayout.addWidget(self._helpButton)

        self._tabsLayout.addWidget(self._tabBar)
        self._tabsLayout.addSpacerItem(
            QtWidgets.QSpacerItem(
                10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
            )
        )
        self._tabsLayout.addWidget(self._rightButtonGroup)

        # stacked widget
        self._stackedWidget = QtWidgets.QStackedWidget(self)

        # Main layout
        self._mainLayout = QtWidgets.QVBoxLayout(self)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setSpacing(5)
        self._mainLayout.addWidget(self._tabsWidget, 0)
        self._mainLayout.addWidget(self._stackedWidget, 1)

        # Connect signals
        self._minRibbonButton.clicked.connect(self._minButtonClicked)
        self._tabBar.currentChanged.connect(
            lambda index: self._stackedWidget.setCurrentIndex(index)
        )

    def setFileTitle(self, title: str):
        """Set the title of the file menu.

        :param title: The title to set.
        """
        self._tabBar.setTabText(0, title)

    def setFileMenu(self, menu: QtWidgets.QMenu):
        """Set the file menu of the ribbon.

        :param menu: The menu to set.
        """
        self._fileMenu = menu
        self._applicationButton.setMenu(menu)

    def addCategory(self, title: str, style=CategoryStyle.Normal) -> Category:
        """Add a new category to the ribbon.

        :param title: The title of the category.
        :param style: The buttonStyle of the category.
        :return: The newly created category.
        """
        category = Category(style, self)
        category.setFixedHeight(self._ribbonHeight -
                                self._tabsWidget.sizeHint().height() -
                                self._mainLayout.spacing() -
                                self._mainLayout.contentsMargins().top() -
                                self._mainLayout.contentsMargins().bottom() - 2)
        self._categories.append(category)
        self._tabBar.addTab(title)
        self._stackedWidget.addWidget(category)
        return category

    def removeCategory(self, category: Category):
        """Remove a category from the ribbon.

        :param category: The category to remove.
        """
        index = self._categories.index(category)
        self._tabBar.removeTab(index)
        self._stackedWidget.removeWidget(self._stackedWidget.widget(index))

    def setCurrentCategory(self, category: Category):
        """Set the current category.

        :param category: The category to set.
        """
        index = self._categories.index(category)
        self._tabBar.setCurrentIndex(index)
        self._stackedWidget.setCurrentIndex(index)

    def addQuickAccessButton(self, button: QtWidgets.QToolButton):
        """Add a widget to the quick access bar.

        :param button: The button to add.
        """
        button.setIconSize(QtCore.QSize(32, 32))
        self._titleBarActions.addWidget(button)

    def setRibbonHeight(self, height: int):
        """Set the total height of the ribbon.

        :param height: The height to set.
        """
        self._ribbonHeight = height
        self.setFixedHeight(height)

    def ribbonHeight(self) -> int:
        """Get the total height of the ribbon.

        :return: The height of the ribbon.
        """
        return self._ribbonHeight

    def setFileIcon(self, icon: QtGui.QIcon):
        """Set the icon of the file menu.

        :param icon: The icon to set.
        """
        self._applicationButton.setIcon(icon)

    def setMinButtonIcon(self, icon: QtGui.QIcon):
        """Set the icon of the min button.

        :param icon: The icon to set.
        """
        self._minRibbonButton.setIcon(icon)

    def removeMinButton(self):
        """Remove the min button from the ribbon."""
        self._minRibbonButton.setVisible(False)

    def setHelpButtonIcon(self, icon: QtGui.QIcon):
        """Set the icon of the help button.

        :param icon: The icon to set.
        """
        self._helpButton.setIcon(icon)

    def removeHelpButton(self):
        """Remove the help button from the ribbon."""
        self._helpButton.setVisible(False)

    def addRightButton(self, button: QtWidgets.QToolButton):
        """Add a widget to the right button bar.

        :param button: The button to add.
        """
        button.setIconSize(QtCore.QSize(32, 32))
        self._rightButtonLayout.addWidget(button)

    def minimumSizeHint(self) -> QtCore.QSize:
        """Return the minimum size hint of the widget.

        :return: The minimum size hint.
        """
        return QtCore.QSize(super().minimumSizeHint().width(), self._ribbonHeight)

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(self.width(), self._ribbonHeight)

    def _minButtonClicked(self):
        if self._stackedWidget.isVisible():
            self._minRibbonButton.setToolTip("Expand Ribbon")
            self._minRibbonButton.setIcon(QtGui.QIcon('icons/expand-arrow.png'))
            self._stackedWidget.setVisible(False)
            self.setFixedSize(self.sizeHint().width(), self._tabsWidget.height())
        else:
            self._minRibbonButton.setToolTip("Collapse Ribbon")
            self._minRibbonButton.setIcon(QtGui.QIcon('icons/collapse-arrow.png'))
            self._stackedWidget.setVisible(True)
            self.setFixedSize(self.sizeHint())
