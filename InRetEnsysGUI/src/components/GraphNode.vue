<script setup>
import { nextTick } from 'vue';

const props = defineProps({
    id: String, 
    classes: String, 
    innerHTML: String
})

nextTick(function() {
    const canvas = document.getElementById("canvas")

    // create new div for graph
    let graphNode = document.createElement("div")

    for (let counter in props.classes) { 
        console.log(props.classes[counter])
        graphNode.classList.add(props.classes[counter])
    }

    graphNode.id = props.id // hier muss dann die ID für die Element generiert werden
    graphNode.innerHTML = props.innerHTML

    // suspend drawing and initialise.
    instance.batch(function () {

        // bind to connection/connectionDetached events, and update the list of connections on screen.
        instance.bind("connection", function (info, originalEvent) {
            updateConnections(info.connection);
        });
        instance.bind("connection:detach", function (info, originalEvent) {
            updateConnections(info.connection, true);
        });

        instance.bind("connection:move", function (info, originalEvent) {
            //  only remove here, because a 'connection' event is also fired.
            // in a future release of jsplumb this extra connection event will not
            // be fired.
            updateConnections(info.connection, true);
        });

        instance.bind("click", function (component, originalEvent) {
            alert("click!")
        });

        // configure some drop options for use by all endpoints.
        var exampleDropOptions = {
            tolerance: "touch",
            hoverClass: "dropHover",
            activeClass: "dragActive"
        };

        //
        // first example endpoint.  it's a 25x21 rectangle (the size is provided in the 'style' arg to the Endpoint),
        // and it's both a source and target.  the 'scope' of this Endpoint is 'exampleConnection', meaning any connection
        // starting from this Endpoint is of type 'exampleConnection' and can only be dropped on an Endpoint target
        // that declares 'exampleEndpoint' as its drop scope, and also that
        // only 'exampleConnection' types can be dropped here.
        //
        // the connection style for this endpoint is a Bezier curve (we didn't provide one, so we use the default), with a strokeWidth of
        // 5 pixels, and a gradient.
        //
        // there is a 'beforeDrop' interceptor on this endpoint which is used to allow the user to decide whether
        // or not to allow a particular connection to be established.
        //
        var exampleColor = "#00f";
        var exampleEndpoint = {
            endpoint: "Rectangle",
            paintStyle: { width: 25, height: 21, fill: exampleColor },
            source: true,
            reattach: true,
            scope: "blue",
            connectorStyle: {
                strokeWidth: 5,
                stroke: exampleColor,
                dashstyle: "2 2"
            },
            target: true,
            beforeDrop: function (params) {
                return confirm("Connect " + params.sourceId + " to " + params.targetId + "?");
            },
            dropOptions: exampleDropOptions
        };

        // setup some DynamicAnchors for use with the blue endpoints
        // and a function to set as the maxConnections callback.
        var anchors = [
                [1, 0.2, 1, 0],
                [0.8, 1, 0, 1],
                [0, 0.8, -1, 0],
                [0.2, 0, 0, -1]
            ],
            maxConnectionsCallback = function (info) {
                alert("Cannot drop connection " + info.connection.id + " : maxConnections has been reached on Endpoint " + info.endpoint.id);
            };

        var e1 = instance.addEndpoint(graphNode, { anchor: anchors }, exampleEndpoint);
        // you can bind for a maxConnections callback using a standard bind call, but you can also supply 'onMaxConnections' in an Endpoint definition - see exampleEndpoint3 above.
        e1.bind("maxConnections", maxConnectionsCallback);

        var windows = document.querySelectorAll(".drag-drop-demo .window");
        for (var i = 0; i < windows.length; i++) {
            instance.addEndpoint(windows[i], exampleEndpoint3);
        }

        var hideLinks = document.querySelectorAll(".drag-drop-demo .hide");
        instance.on(hideLinks, "click", function (e) {
            instance.toggleVisible(this.parentNode);
            instance.consume(e);
        });

        var dragLinks = document.querySelectorAll(".drag-drop-demo .drag");
        instance.on(dragLinks, "click", function (e) {
            var s = instance.toggleDraggable(this.parentNode);
            this.innerHTML = (s ? 'disable dragging' : 'enable dragging');
            instance.consume(e);
        });

        var detachLinks = document.querySelectorAll(".drag-drop-demo .detach");
        instance.on(detachLinks, "click", function (e) {
            instance.deleteConnectionsForElement(this.parentNode);
            instance.consume(e);
        });

        instance.on(document.getElementById("clear"), "click", function (e) {
            instance.deleteEveryConnection();
            showConnectionInfo("");
            instance.consume(e);
        });

    });
    
    canvas.appendChild(graphNode)
})
</script>


<template>
    <!-- 
        <br/>
        <br/>
        <a href="#" class="cmdLink hide" rel="dragDropWindow2">toggle connections</a>
        <br/>
        <a href="#" class="cmdLink drag" rel="dragDropWindow2">disable dragging</a>
        <br/>
        <a href="#" class="cmdLink detach" rel="dragDropWindow2">detach all</a>
    -->
</template>

<style>

</style>