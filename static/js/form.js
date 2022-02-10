let options = {
    'int': 'Integer',
    'float': 'Float',
    'str': 'String',
    'bool': 'Boolean'
}

function addPropertyInputHTML(id, value, fieldset) {

    label_node = document.createElement("label");
    label_node.innerHTML = value;
    label_node.htmlFor = value;

    fieldset.append(label_node);

    select_node = document.createElement("select");
    select_node.classList.add('property-value')
    select_node.name = value
    select_node.dataset.name = value;
    select_node.dataset.class = id;

    Object.keys(options).forEach((key) => {
        option = document.createElement("option");
        option.value = key;
        option.innerHTML = options[key]
        select_node.options.add(option);
    })

    fieldset.append(select_node)
}

function getFormData() {
    // Get generation form
    let form = document.getElementById('generate-form');

    // Get all class divs
    let classes = document.querySelectorAll('.class-value');

    // Extract form data
    let data = new FormData(form);

    // Create class object for
    let class_object = {};

    // For each class div element
    classes.forEach(element => {

        // Extract classId from div
        let classId = element.dataset.value;

        // Create new sun class object
        class_object[classId] = {};

        // Get all assigned properties
        let properties = document.querySelectorAll('.property-value[data-class=' + classId + ']');

        // For each class property
        properties.forEach(property => {
            // Extract property data and append to class object.
            class_object[classId][property.dataset.name] = property.value;
        })
    })

    // Append classes as json string
    data.append('classes', JSON.stringify(class_object));

    return data;
}

function download_element(path, name) {
    const a = document.createElement('a');
    a.href = path;
    a.download = name;
    a.target = 'blank';
    // TODO: REMOVE DEBUG
    console.log(a);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

document.addEventListener('DOMContentLoaded', (e) => {

    // Submit button
    let update_url = document.querySelector('#update-url');

    let generate_elements = document.querySelectorAll('.generate-element');

    generate_elements.forEach(
        (element) => {
            element.addEventListener('change', (e) => {

                // Get preview code element
                let preview = document.getElementById('generate-preview');

                // Get request url from button
                let url = update_url.dataset.url;

                let data = getFormData();

                fetch(url, {
                    method: 'POST',
                    body: data
                })
                    .then((response) => response.text())
                    .then(data => {
                        preview.innerText = data;
                    })
            })
        }
    )

    // Generate Button

    let generate_button = document.querySelector('#generate-submit')

    generate_button.addEventListener('click', (e) => {

        // Set loading state
        generate_button.ariaBusy = 'true';

        let url = generate_button.dataset.url;

        let data = getFormData();

        fetch(url, {
            method: 'POST',
            body: data
        })
            .then((response) => response.json())
            .then(data => {
                 // Set loading state
                generate_button.ariaBusy = 'false';

                // Trigger Download
                download_element(data['url'], data['name']);
            })
    })

    // Property buttons

    let add_property_buttons = document.querySelectorAll('.add-property-btn')

    add_property_buttons.forEach(button => {

        let id = button.dataset.id
        let input = document.querySelector('.add-property-input[data-id=' + id + ']')
        let fieldset = document.querySelector('.property-set[data-id=' + id + ']')

        button.addEventListener('click', (e) => {
            if (input.value) {
                let data = new FormData()
                data.append('property', input.value)

                addPropertyInputHTML(id, input.value, fieldset)
                fieldset.style.display = 'block'
                input.value = ''
                input.dispatchEvent(new Event('change'))

                /*  fetch(url, {
                      method: 'POST', body: data
                  }).then((response) => response.json())
                      .then(data => {
                          fieldset.style.display = 'block'
                          fieldset.innerHTML += data.template;
                          input.value = ""
                      })*/
            }
        })
    })

})