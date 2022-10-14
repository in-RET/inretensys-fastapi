
nextTick(function (){
    let counter=5;		

    var instance = window.j = jsPlumbBrowserUI.newInstance({
        dragOptions: { cursor: 'pointer', zIndex: 2000 },
        paintStyle: { stroke: '#666' },
        endpointHoverStyle: { fill: "orange" },
        hoverPaintStyle: { stroke: "orange" },
        endpointStyle: { width: 20, height: 16, stroke: '#666' },
        endpoint: "Rectangle",
        anchors: ["TopCenter", "TopCenter"],
        container: canvas,
        dropOptions:{activeClass:"dragActive", hoverClass:"dropHover"}
    });

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
        var exampleEndpoint = { //blue endpoint for source and transformer with 'source:true' 
        //so it can not be used as target
            endpoint: "Rectangle",
            paintStyle: { width: 25, height: 21, fill: exampleColor },
            source: true,
            reattach: true,
            scope: "blue",
            connectorStyle: {
                strokeWidth: 5,
                stroke: exampleColor,
                //dashstyle: "2 2"
            },
            connector: "Flowchart",
            beforeDrop: function (params) {
                connect_info(params.sourceId, params.targetId);
                return confirm("Connect " + params.sourceId + " to " + params.targetId + "?");
            },
            dropOptions: exampleDropOptions
        };


        var exampleColor = "#00f";
        var exampleEndpoint_Bus = { //blue endpoint of bus
            endpoint: "Rectangle",
            paintStyle: { width: 25, height: 21, fill: exampleColor },
            reattach: true,
            scope: "blue",
            connectorStyle: {
                strokeWidth: 5,
                stroke: exampleColor,
                //dashstyle: "2 2"
            },
            connector: "Flowchart",
            source: true,
            target: true,
            maxConnections: 10,
            beforeDrop: function (params) {
                connect_info(params.sourceId, params.targetId);
                return confirm("Connect " + params.sourceId + " to " + params.targetId + "?");
            },
            dropOptions: exampleDropOptions
        };


        //
        // the second example uses a Dot of radius 15 as the endpoint marker, is both a source and target,
        // and has scope 'exampleConnection2'.
        //
        var color2 = "#316b31";
        var exampleEndpoint2 = { // green endpoint of sink which can only be used as target (target:true)
            endpoint: {type:"Dot", options:{ radius: 11 }},
            paintStyle: { fill: color2 },
            //source: true,
            scope: "green",
            connectorStyle: { stroke: color2, strokeWidth: 6 },
            connector: "Flowchart",//{type:"Bezier", options:{ curviness: 63 } },
            maxConnections: 1,
            target: true,
            beforeDrop: function (params) {
                connect_info_bus_to_sink(params.sourceId, params.targetId);
                return confirm("Connect " + params.sourceId + " to " + params.targetId + "?");
            },
            dropOptions: exampleDropOptions
        };

        var exampleEndpoint2_Bus = { // green endpoint of bus which is the 'source'
            endpoint: {type:"Dot", options:{ radius: 11 }},
            paintStyle: { fill: color2 },
            source: true,
            scope: "green",
            connectorStyle: { stroke: color2, strokeWidth: 6 },
            connector: "Flowchart",
            maxConnections: 3,
            //target: true,
            beforeDrop: function (params) {
                connect_info_bus_to_sink(params.sourceId, params.targetId);
                return confirm("Connect " + params.sourceId + " to " + params.targetId + "?");
            },
            dropOptions: exampleDropOptions
        };

        //
        // the third example uses a Dot of radius 17 as the endpoint marker, is both a source and target, and has scope
        // 'exampleConnection3'.  it uses a Straight connector, and the Anchor is created here (bottom left corner) and never
        // overriden, so it appears in the same place on every element.
        //
        // this example also demonstrates the beforeDetach interceptor, which allows you to intercept
        // a connection detach and decide whether or not you wish to allow it to proceed.
        //
        var example3Color = "rgba(229,219,61,0.5)";
        var exampleEndpoint3 = { // yellow endpoint
            endpoint: {type:"Dot", options:{radius: 17} },
            anchor: "Left",
            paintStyle: { fill: example3Color, opacity: 0.5 },
            source: true,
            scope: 'yellow',
            connectorStyle: {
                stroke: example3Color,
                strokeWidth: 4
            },
            connector: "Flowchart",
            //target: true,
            dropOptions: exampleDropOptions,
            beforeDetach: function (conn) {
                return confirm("Detach connection?");
            },
            beforeDrop: function (params) {
                connect_info(params.sourceId, params.targetId);
                return confirm("Connect " + params.sourceId + " to " + params.targetId + "?");
            },
            onMaxConnections: function (info) {
                alert("Cannot drop connection " + info.connection.id + " : maxConnections has been reached on Endpoint " + info.endpoint.id);
            }
        };

        var exampleEndpoint3_Bus = { // yellow endpoint
            endpoint: {type:"Dot", options:{radius: 17} },
            anchor: "Left",
            paintStyle: { fill: example3Color, opacity: 0.5 },
            //source: true,
            scope: 'yellow',
            connectorStyle: {
                stroke: example3Color,
                strokeWidth: 4
            },
            connector: "Flowchart",
            target: true,
            dropOptions: exampleDropOptions,
            beforeDetach: function (conn) {
                return confirm("Detach connection?");
            },
            beforeDrop: function (params) {
                connect_info(params.sourceId, params.targetId);
                return confirm("Connect " + params.sourceId + " to " + params.targetId + "?");
            },
            onMaxConnections: function (info) {
                alert("Cannot drop connection " + info.connection.id + " : maxConnections has been reached on Endpoint " + info.endpoint.id);
            }
        };


        var exampleColor4 = "#ff7b5a";//orange
        var exampleEndpoint4 = { 
            endpoint: "Rectangle",
            anchor: "Left",
            paintStyle: { fill: exampleColor4, opacity: 0.5 },
            source: true,
            //scope: 'yellow',
            connectorStyle: {
                stroke: exampleColor4,
                strokeWidth: 4
            },
            connector: "Flowchart",
            target: true,
            dropOptions: exampleDropOptions,
            beforeDetach: function (conn) {
                return confirm("Detach connection?");
            },
            beforeDrop: function (params) {
                connect_info_bus_to_storage(params.sourceId, params.targetId);
                return confirm("Connect " + params.sourceId + " to " + params.targetId + "?");
            },
            onMaxConnections: function (info) {
                alert("Cannot drop connection " + info.connection.id + " : maxConnections has been reached on Endpoint " + info.endpoint.id);
            }
        };


        var exampleColor5 = "#B80F0A";//red
        var exampleEndpoint5 = { 
            endpoint: "Rectangle",
            anchor: "Left",
            paintStyle: { fill: exampleColor5, opacity: 0.5 },
            source: true,
            //scope: 'yellow',
            connectorStyle: {
                stroke: exampleColor5,
                strokeWidth: 4
            },
            connector: "Flowchart",
            target: true,
            dropOptions: exampleDropOptions,
            beforeDetach: function (conn) {
                return confirm("Detach connection?");
            },
            onMaxConnections: function (info) {
                alert("Cannot drop connection " + info.connection.id + " : maxConnections has been reached on Endpoint " + info.endpoint.id);
            }
        };


        var dd1 = document.getElementById('SourceWindow1'),
            dd2 = document.getElementById('SourceWindow2'),
            dd3 = document.getElementById('BusWindow3'),
            dd4 = document.getElementById('SinkWindow4'),
            dd5 = document.getElementById('StorageWindow5');

        // setup some empty endpoints.  again note the use of the three-arg method to reuse all the parameters except the location
        // of the anchor (purely because we want to move the anchor around here; you could set it one time and forget about it though.)

        //instance.addEndpoint(dd1, { anchor: [0.5, 1, 0, 1] }, exampleEndpoint2);

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

        var e1 = instance.addEndpoint(dd1, { anchor: anchors }, exampleEndpoint);
        // you can bind for a maxConnections callback using a standard bind call, but you can also supply 'onMaxConnections' in an Endpoint definition - see exampleEndpoint3 above.
        e1.bind("maxConnections", maxConnectionsCallback);

        /////////////////////////////////////////////////////////////////////////////////////

        dd1.addEventListener("dblclick", openForm_Source);
        dd2.addEventListener("dblclick", openForm_Source);
        dd3.addEventListener("dblclick", openForm_Bus);
        dd4.addEventListener("dblclick", openForm_Sink);
            
        function openForm_Source() {
            document.getElementById("popupForm_Source").style.display = "block";
            document.getElementById("label_source").focus();
        }

        function openForm_Sink() {
            document.getElementById("popupForm_Sink").style.display = "block";
            document.getElementById("label_sink").focus();
        }

        function openForm_Bus() {
            document.getElementById("popupForm_Bus").style.display = "block";
            document.getElementById("label_bus").focus();
        }

        /////////////////////////////////////////////////////////////////////////////////////

        //var e2 = instance.addEndpoint(dd2, { anchor: [0.5, 1, 0, 1] }, exampleEndpoint);
        // again we bind manually. it's starting to get tedious.  but now that i've done one of the blue endpoints this way, i have to do them all...
        //e2.bind("maxConnections", maxConnectionsCallback);
        //instance.addEndpoint(dd2, { anchor: "Right" }, exampleEndpoint2);

        var e3 = instance.addEndpoint(dd3, { anchor: [0.25, 0, 0, -1] }, exampleEndpoint_Bus);
        e3.bind("maxConnections", maxConnectionsCallback);
        instance.addEndpoint(dd3, { anchor: [0.75, 0, 0, -1] }, exampleEndpoint2_Bus);


        //var e4 = instance.addEndpoint(dd4, { anchor: [1, 0.5, 1, 0] }, exampleEndpoint);
        //e4.bind("maxConnections", maxConnectionsCallback);
        instance.addEndpoint(dd4, { anchor: [0.25, 0, 0, -1] }, exampleEndpoint2);
                        
        instance.addEndpoint(dd2, { anchor: anchors }, exampleEndpoint3); //the round yellow one
        instance.addEndpoint(dd3, { anchor: anchors }, exampleEndpoint3_Bus); //the round yellow one

        instance.addEndpoint(dd5, { anchor: anchors }, exampleEndpoint4); //storage stuff
        instance.addEndpoint(dd5, { anchor: "Left" }, exampleEndpoint5);
        instance.addEndpoint(dd3, { anchor: anchors }, exampleEndpoint4);
        instance.addEndpoint(dd3, { anchor: "Right" }, exampleEndpoint5);

        $(function() {
        $('#btn_new_source').click(function(){
                var newDiv = $('<div class="window" id="new_source"><h4><a>New Source</a></h4> </div>');
                //newDiv.style.background = "#000";
                $('#canvas').append(newDiv);
                //newDiv.id="new_source"+counter;
                document.getElementById('new_source').id = 'new_source'+counter;
                //document.getElementById("new_source").setAttribute("id", "new_source"+counter);
                //alert(newDiv.id);
                var windows = document.querySelectorAll(".drag-drop-demo .window");
                //alert(windows.length);
                //dd6 = document.getElementById(newDiv.id.toString());
                instance.addEndpoint(windows[counter], { anchor: "Right" }, exampleEndpoint5);
                counter++;
                //alert(counter);
            });
        });

        var windows = document.querySelectorAll(".drag-drop-demo .window");
        //for (var i = 0; i < windows.length; i++) {
            //  instance.addEndpoint(windows[i], exampleEndpoint3); //the round yellow one
        //}

        //var hideLinks = document.querySelectorAll(".drag-drop-demo .hide");
        //instance.on(hideLinks, "click", function (e) {
            //  instance.toggleVisible(this.parentNode);
            //instance.consume(e);
        //});

        //var dragLinks = document.querySelectorAll(".drag-drop-demo .drag");
        //instance.on(dragLinks, "click", function (e) {
            //  var s = instance.toggleDraggable(this.parentNode);
            //this.innerHTML = (s ? 'disable dragging' : 'enable dragging');
            //instance.consume(e);
        //});

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
    })
})