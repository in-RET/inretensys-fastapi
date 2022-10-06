// declarations
const backend_ip = "127.0.0.1:8000"

window.onload = init

function init() {
    listComponents()
}

async function getSchema(url){
    var debug = false

    let schema = await fetchData(url);
    
    let json_schema = JSON.parse(schema);
    // console.log("JSON Objekt:")
    console.log(json_schema)

    // wir haben hier ein Fancy Schema und müssen nun eine Form bauen
    let content = document.getElementById("content");
    content.innerHTML = "";

    let form = document.createElement("form")
    form.method = "POST"

    for (let key in json_schema.properties) {
        for (let childkey in json_schema.properties[key]) {
            switch (childkey){
                case "title":
                    prop_info = document.createElement("h4");
                    prop_info.innerText = json_schema.properties[key][childkey];
    
                    if (json_schema.hasOwnProperty("required")){
                        console.log("required vorhanden: " + json_schema.properties[key])
                        if (json_schema.required.includes(json_schema.properties[key])){
                            prop_info.innerText = prop_info.innerText + "(Erforderlich)";
                        }
                    }

                    form.appendChild(prop_info);
                    form.appendChild(document.createElement("hr"))
                    break;

                case "type":
                    prop_label = document.createElement("label")
                    prop_label.for = json_schema.properties[key]["title"]
                    prop_label.innerText = "Value:"

                    form.appendChild(prop_label)
                    switch (json_schema.properties[key]["type"]){
                        case "string":
                            prop_datafield = document.createElement("input")
                            prop_datafield.type = "text"
                            prop_datafield.name = json_schema.properties[key]["title"]
                            
                            form.appendChild(prop_datafield)
                            break;

                        case "boolean":
                            prop_datafield = document.createElement("input")
                            prop_datafield.type = "checkbox"
                            prop_datafield.name = json_schema.properties[key]["title"]

                            form.appendChild(prop_datafield)
                            break;

                        case "number" || "integer":
                            prop_datafield = document.createElement("input")
                            prop_datafield.type = "range"
                            prop_datafield.min = json_schema.properties[key]["minimum"]
                            prop_datafield.max = json_schema.properties[key]["maximum"]
                            prop_datafield.step = json_schema.properties[key]["step"]
                            prop_datafield.name = json_schema.properties[key]["title"]

                            form.appendChild(prop_datafield)

                            break;
                    }
                    break;

                default:
                    if (debug) {
                        prop_info = document.createElement("p");
                        prop_info.innerText = childkey + ": " + json_schema.properties[key][childkey];
    
                        form.appendChild(prop_info);
                    }    
            }
        }

        form.append(document.createElement("br"))
    }

    form.append(document.createElement("br"))

    let submit_btn = document.createElement("button")
    submit_btn.type = "submit"
    submit_btn.innerText = "Speichern"

    form.appendChild(submit_btn)
    content.appendChild(form)
}

async function listComponents(){
    let componentslist = await fetchData('http://' + backend_ip + '/getComponentsList');

    componentslist.components.forEach(element => {
        // Create URL for the Schematic
        var link = 'http://' + backend_ip + '/getComponentSchema/' + element

        // Create Link with all data
        const a = document.createElement('a');
        a.id = element;
        a.innerHTML = element;
        a.setAttribute("onclick", "getSchema('" + link + "')");

        // Create and add Link to List-Item
        const li = document.createElement('li')
        li.appendChild(a)

        // Listenelement zum füllen mit Einträgen
        let list = document.getElementById("componentlist");
        list.appendChild(li);   
    });
}

async function fetchData(url) {
    let response = await fetch(url);
    let data = await response.json();

    return data
}