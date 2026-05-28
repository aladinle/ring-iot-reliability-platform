import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    id: root
    width: 1200
    height: 760
    visible: true
    title: "Ring IoT Reliability Dashboard"

    Column {
        anchors.fill: parent
        spacing: 12
        padding: 16

        Label {
            text: "Fleet Health"
            font.pixelSize: 24
            font.bold: true
        }

        Label {
            text: "Dashboard shell placeholder. Python dashboard models and API client provide the data contract for this Qt view."
            wrapMode: Text.WordWrap
        }
    }
}

