var months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"];

function populateTab() {
    let selected_courses = []
    $.ajax({
        type: "GET",
        url: '/data',
        success: function (response) {
            document.querySelector('h1').innerHTML = months[response.monat - 1] + " " + response.jahr

            let main_tab = document.querySelector('table')
            let body = main_tab.createTBody()
            for (let row of response.kurse) {
                let tab_row = body.insertRow();

                let date = new Date(response.jahr, response.monat, row.tag)

                //Date
                let date_cell = tab_row.insertCell();
                date_cell.innerHTML = '<b>' + row.tag + " " + date.toLocaleDateString('de-DE', { weekday: 'long' }) + '</b>';


                tab_row = body.insertRow();
                for (let sub_row of row.maeglichkeiten) {

                    //tick
                    tab_row = body.insertRow();

                    let cell = tab_row.insertCell();

                    let chk_div = document.createElement('div')
                    chk_div.className = "form-check form-switch"

                    let chk_box = document.createElement('input')
                    chk_box.dataset.id = sub_row.id


                    chk_box.type = "checkbox"
                    chk_box.addEventListener('change', function () {
                        if (this.checked) {
                            selected_courses.push(chk_box.dataset.id)
                        }
                        else {
                            selected_courses.pop(chk_box.dataset.id)
                        }
                    });

                    chk_box.className = "form-check-input"
                    chk_div.append(chk_box)
                    cell.append(chk_div)



                    let begin_date = date
                    begin_date.setHours(sub_row.begin.uhr, sub_row.begin.minuten)

                    let end_date = date
                    end_date.setHours(sub_row.begin.uhr, sub_row.begin.minuten)

                    cell = tab_row.insertCell();
                    cell.innerHTML = begin_date.toTimeString().split(' ')[0].substring(0, 5) + " ⇀ " + end_date.toTimeString().split(' ')[0].substring(0, 5);

                    cell = tab_row.insertCell();

                    if (sub_row.bemerkung != null) {
                        cell.innerHTML = sub_row.name + '<br> <b>*' + sub_row.bemerkung + '</b>'
                    }
                    else {
                        cell.innerHTML = sub_row.name
                    }
                }


            }
        }, error: function (xhr) {
            alert("Error" + xhr.status + ' : ' + xhr.responseText);
        }



    })
    document.querySelector("form").addEventListener('formdata', (e) => {

        e.formData.append("courses", JSON.stringify(selected_courses));
        e.formData.append("email", document.querySelector("#emailInput").value);
    });

}

populateTab()