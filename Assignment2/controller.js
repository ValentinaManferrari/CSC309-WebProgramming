//////////////////////////////////////////////////////////////////////////////////////
//////////////////                     PART 1                      ///////////////////
//////////////////////////////////////////////////////////////////////////////////////
$( document ).ready(function() {
    // array of flags to keep track of filed correctness in the respective order (username, pwd1, pwd2, email, phone)
    // flag is set to true only if the field is valid
    let flags = [false, false, false, false, false];

    var username = document.getElementById("username");
    username.addEventListener('keyup', (event) => {
        // Username must be at least six characters long 
        // and only consist of letters (lowercase or uppercase), digits, and underscore. 
        var username_value = event.target.value;
        var p_username = document.getElementById('username_notification');
        var format = /[ `!@#$%^&*()+\-=\[\]{};':"\\|,.<>\/?~]/;
        
        if (username_value.length < 6 || format.test(username_value)){
            p_username.innerHTML = "Username is invalid";
            // p_username.style.display = 'block';
            username.style.backgroundColor = 'red';
            // username.style.borderColor = 'red';
            flags[0] = false;
        }else{
            p_username.innerHTML = "";
            // p_username.style.display = 'none';
            username.style.backgroundColor = '';
            // username.style.borderColor = '';
            flags[0] = true;
        }
    })

    var password1 = document.getElementById('password1');
    password1.addEventListener('keyup', (event) => {
        // must be at least eight characters long, and it must include at least 
        // one digit, one lowercase letter, one uppercase letter, and one sign (i.e., a character from the set !@#$%^&*)
        var password1_value = event.target.value;
        var p_password1 = document.getElementById('password1_notification');
        var hasNumber = /\d/;
        var specialCase = /[!@#$%^&*]/;
        var isUpperCase = /[A-Z]/;
        var isLowerCase = /[a-z]/;
        if (password1_value.length < 8 || !hasNumber.test(password1_value) || !specialCase.test(password1_value) 
                    || !isUpperCase.test(password1_value) || !isLowerCase.test(password1_value)){
            p_password1.innerHTML ="Password is invalid";
            // p_password1.style.display = 'block';
            password1.style.backgroundColor = 'red';
            // password1.style.borderColor = 'red';
            flags[1] = false;
        }else{
            p_password1.innerHTML = "";
            // p_password1.style.display = 'none';
            password1.style.backgroundColor = '';
            // password1.style.borderColor = '';
            flags[1] = true;
        }

        // if password1 is changed and is now different from password 2 
        // raise error in password 2 field
        var p_password2 = document.getElementById('password2_notification');
        if(password1_value != password2.value){
            p_password2.innerHTML ="Passwords don't match";
            // p_password2.style.display = "block";
            password2.style.backgroundColor = 'red';
            // password2.style.borderColor = 'red';
            flags[2] = false;
        }else{
            p_password2.innerHTML = "";
            // p_password2.style.display = "none";
            password2.style.backgroundColor = '';
            // password2.style.borderColor = '';
            flags[2] = true;
        }
    })

    var password2 = document.getElementById('password2');
    password2.addEventListener('keyup', (event) => {
        // Repeat password must be equal to password.
        var password2_value = event.target.value;
        var password1_value = password1.value;
        var p_password2 = document.getElementById('password2_notification');
        if (password2_value !== password1_value || password2_value == ""){
            p_password2.innerHTML ="Passwords don't match";
            // p_password2.style.display = 'block';
            password2.style.backgroundColor = 'red';
            // password2.style.borderColor = 'red';
            flags[2] = false;
        }else{
            p_password2.innerHTML = "";
            // p_password2.style.display = 'none';
            password2.style.backgroundColor = '';
            // password2.style.borderColor = '';
            flags[2] = true;
        }
    })

    let email = document.getElementById("email");
    email.addEventListener('keyup', (event) => {
        // Email must be a valid email address.
        var email_value = event.target.value;
        var p_email = document.getElementById('email_notification');
        var isValidEmail = /\S+@\S+\.\S+/;

        if (!isValidEmail.test(email_value)){
            p_email.innerHTML ="Email is invalid";
            // p_email.style.display = 'block';
            email.style.backgroundColor = 'red';
            // email.style.borderColor = 'red';
            flags[3] = false;
        }else{
            p_email.innerHTML = "";
            // p_email.style.display = 'none';
            email.style.backgroundColor = '';
            // email.style.borderColor = '';
            flags[3] = true;
        }
    })

    let phone = document.getElementById('phone');
    phone.addEventListener('keyup', (event) => {
        // Phone must follow the following format: ???-???-????, where each ? is a digit.
        var phone_value = event.target.value;
        var p_phone = document.getElementById('phone_notification');
        var isValidPhone = /(\d{3})[-](\d{3})[-](\d{4})/;

        if (!isValidPhone.test(phone_value)){
            p_phone.innerHTML ="Phone is invalid";
            // p_phone.style.display = 'block';
            phone.style.backgroundColor = 'red';
            // phone.style.borderColor = 'red';
            flags[4] = false;
        }else{
            p_phone.innerHTML = "";
            // p_phone.style.display = 'none';
            phone.style.backgroundColor = '';
            // phone.style.borderColor = '';
            flags[4] = true;
        }
    })
    
    let submit_button = document.getElementById('register');
    submit_button.onclick = function(){
        // validate all fields before sending a request
        var p_submit = document.getElementById('notification');

        if(!flags.every(Boolean)){
            p_submit.innerHTML ="At least one field is invalid. Please correct it before proceeding";
            p_submit.style.display = 'block';
            for(i=0; i<flags.length; i++){
                flag = flags[i];
                if(flag === false){
                    if(i == 0){
                        document.getElementById('username_notification').innerHTML = "Username is invalid";
                        username.style.backgroundColor = 'red';
                    }else if(i == 1){
                        document.getElementById('password1_notification').innerHTML = "Password is invalid";
                        password1.style.backgroundColor = 'red';
                    }else if(i == 2){
                        document.getElementById('password2_notification').innerHTML = "Passwords don't match";
                        password2.style.backgroundColor = 'red';
                    }else if(i == 3){
                        document.getElementById('email_notification').innerHTML = "Email is invalid";
                        email.style.backgroundColor = 'red';
                    }else if(i == 4){
                        document.getElementById('phone_notification').innerHTML = "Phone is invalid";
                        phone.style.backgroundColor = 'red';
                    }
                }
            }
            return;
        }
        
        // submit form
        $.ajax({
            url : "https://csc309.teach.cs.toronto.edu/a2/register",
            method : "POST",
            // dataType : "application/json",
            data: {"username": username.value, "password1": password1.value, "password2": password2.value, "email": email.value, "phone": phone.value},
            statusCode: {
                200: function(responseObject, textStatus, jqXHR) {
                    p_submit.innerHTML = "User added"
                    p_submit.style.visibility = "visible";
                },
                404: function(responseObject, textStatus, jqXHR) {
                    p_submit.innerHTML = "Unknown error occurred"
                    p_submit.style.visibility = "visible";
                },
                409: function(responseObject, textStatus, jqXHR) {
                    p_submit.innerHTML = "Username has already been taken"
                    p_submit.style.visibility = "visible";
                }           
            }
        })
    }
});

//////////////////////////////////////////////////////////////////////////////////////
//////////////////                     PART 2                      ///////////////////
//////////////////////////////////////////////////////////////////////////////////////
// initialize list of items for products displayed in the table
var itemsList = [];
$( document ).ready(function() {
    let add_update_button = document.getElementById('add_update_item');
    add_update_button.onclick = function(){
        // get fields values
        let name = document.getElementById('name').value;
        name = name.replace(/\s+/g, '_'); // replace spaces with underscores in product name
        let price = document.getElementById('price').value;
        let quantity = document.getElementById('quantity').value;
        // if any field is empty skip button action
        if(name === "" || price === "" || quantity === ""){
            return;
        }
        // create new item object with retrieved inputs
        item = new Item(name, price, quantity);
        item.total = Number(item.total).toFixed(2);
        // update item in table if it already exist
        if(itemsList.find(item => item.name === name)){
            // update item values in list
            let old_item = itemsList.find(item => item.name === name)
            old_item.price = item.price;
            old_item.quantity = item.quantity;
            // update subtotal, taxes and grand total
            old_item.total = item.total;
            totals();
            // display new values in table
            var row = document.getElementById(old_item.name);
            row.getElementsByTagName("td")[1].innerHTML = old_item.price;
            row.getElementsByTagName("td")[2].innerHTML = old_item.quantity;
            row.getElementsByTagName("td")[3].innerHTML = old_item.total;
        }
        // add new item in table if it has a new name
        else{ 
            // add new item to itemList
            itemsList.push(item);
            // create new table row 
            var table = document.getElementById('cart-items').getElementsByTagName('tbody')[0];
            var row = table.insertRow();
            row.id = name;
            // add cell for name and add value
            var nameCell = row.insertCell(0);
            nameCell.innerHTML = item.name;
            // add cell for price and add value
            var priceCell = row.insertCell(1);
            priceCell.innerHTML = item.price;
            // add cell for quantity and add value
            var quantityCell = row.insertCell(2);
            quantityCell.innerHTML = item.quantity;
            // add cell for total and add value
            var totalCell = row.insertCell(3);
            totalCell.innerHTML = item.total;
            // create button for decrease quantity
            var minusCell = row.insertCell(4);
            var minusButton = document.createElement("button");
            minusButton.type = "button";
            minusButton.setAttribute("class", "decrease");
            minusButton.setAttribute("onclick", "decrease("+JSON.stringify(item.name)+")");
            minusButton.innerHTML ="-";
            minusCell.appendChild(minusButton);
            // create button for increase quantity
            var plusCell = row.insertCell(5);
            var plusButton = document.createElement("button");
            plusButton.type = "button";
            plusButton.setAttribute("class","increase");
            plusButton.setAttribute("onclick", "increase("+JSON.stringify(item.name)+")");
            plusButton.innerHTML ="+";
            plusCell.appendChild(plusButton);
            // create button for deleting table row
            var deleteCell = row.insertCell(6);
            var deleteButton = document.createElement("button");
            deleteButton.type = "button";
            deleteButton.setAttribute("class","delete");
            deleteButton.setAttribute("onclick", "deleteRow("+JSON.stringify(item.name)+")");
            deleteButton.innerHTML ="delete";
            deleteCell.appendChild(deleteButton);
            // calculate subtotal, taxtes and grand total 
            totals();
        }
    }
}); 
// function to calculate and display subtotal, taxes and grand total 
function totals(){
    // convert current values from strings to numbers
    let subtotal = 0;
    let taxes = 0;
    let grand_total = 0;
    
    for(i=0; i<itemsList.length; i++){
        subtotal += Number(itemsList[i].total);
    }
    taxes = subtotal * (0.13); // taxes are 13%
    grand_total = subtotal + taxes; 
    // display results in html rounding to 2 decimal numbers
    document.getElementById("subtotal").innerHTML = subtotal.toFixed(2);
    document.getElementById("taxes").innerHTML = taxes.toFixed(2);
    document.getElementById("grand_total").innerHTML = grand_total.toFixed(2);
}
// function to decrease quantity given an item name/id (also updates item values in itemList)
function decrease(name){
    var item = itemsList.filter(item => item.name === name)[0];
    // decrease quantity only if it is not already zero
    if(item.quantity > 0){
        // decrease quantity by one and display new value in table cell
        item.quantity = item.quantity - 1;
        var quantityCell = document.getElementById(item.name).getElementsByTagName("td")[2];
        quantityCell.innerHTML = item.quantity;
        // adjust item total and display new value in table cell
        item.total = Number(item.quantity * item.price).toFixed(2);
        var totalCell = document.getElementById(item.name).getElementsByTagName("td")[3];
        totalCell.innerHTML = item.total;
        // adjust overall totals and display values
        totals();
    }
}
// function to increase quantity given an item name/id (also updates item values in itemList)
function increase(name){
    var item = itemsList.filter(item => item.name === name)[0];
    // increase quantity by one and display new value in table cell
    item.quantity = Number(item.quantity) + 1;
    var quantityCell = document.getElementById(item.name).getElementsByTagName("td")[2];
    quantityCell.innerHTML = item.quantity;
    // adjust item total and display new value in table cell
    item.total = Number(item.quantity * item.price).toFixed(2);
    var totalCell = document.getElementById(item.name).getElementsByTagName("td")[3];
    totalCell.innerHTML = item.total;
    // adjust overall totals and display values
    totals();
}
// function to delete table row given an item name/id (also updates item values in itemList)
function deleteRow(name){
    // delete row in table
    row = document.getElementById(name);
    row.remove();
    // delete item from itemList
    const indexOfItem = itemsList.findIndex(item => item.name === name);   
    itemsList.splice(indexOfItem, 1);
    // adjust overall totals and display values
    totals();
}

//////////////////////////////////////////////////////////////////////////////////////
//////////////////                     PART 3                      ///////////////////
//////////////////////////////////////////////////////////////////////////////////////
$( document ).ready(function() {
    // control variables
    let number = 1;
    let hasNext = true;
    // ajax call to get next 5 paragraphs or display end line
    function getParagraphs(number){
        $.ajax({
            url : "https://csc309.teach.cs.toronto.edu/a2/text/data?paragraph="+ number,
            method : "GET",
            success: function(response){
                // show 5 paragraphs
                for(i=0; i < response.data.length; i++){
                    var info_paragraph = response.data.at(i);
                    // create div with id "paragraph_#"
                    let div = document.createElement("div");
                    div.id = "paragraph_" + info_paragraph.paragraph;
                    // create p for paragraph content
                    let p = document.createElement("p");
                    p.innerHTML = info_paragraph.content;
                    // diplay paragraph # in bold
                    let b = document.createElement("b");
                    b.innerHTML = "(Paragraph: " + info_paragraph.paragraph + ")";
                    // create like button
                    let button = document.createElement("button");
                    button.setAttribute("class", "like");
                    button.innerHTML = "Likes " + info_paragraph.likes;
                    button.setAttribute("onclick", "addLike("+info_paragraph.paragraph+")");
                    // append newly created elements
                    p.appendChild(b);
                    div.appendChild(p);
                    div.appendChild(button);
                    document.getElementById("data").appendChild(div);
                }
                // check if there are more paragraphs
                hasNext = response.next;
                // if not, show end message. (else --> continue)
                if(!hasNext){
                    let p = document.createElement("p");
                    let b = document.createElement("b");
                    b.innerHTML = "You have reached the end";
                    p.appendChild(b);
                    document.getElementById("data").appendChild(p);
                }            
            },
            error: function(){
                console.log("Error: API call failed (GET)");
            }
        });
    } 
    // initialize first paragraphs set display
    getParagraphs(number);
    // happens when scrolling - call getPharagraphs()
    window.addEventListener('scroll', () => {
        const {
            scrollTop,
            scrollHeight,
            clientHeight
        } = document.documentElement;
        // if there are more paragraphs to display
        if (scrollTop + clientHeight >= scrollHeight - 5 && hasNext) {
            // get new paragraphs
            number = number + 5;
            getParagraphs(number);
        }
    }, {
        passive: true
    });
});
// function to increase number of likes when like button is pressed
function addLike(paragraph_number){
    // post call to get likes info
    $.ajax({
        url : "https://csc309.teach.cs.toronto.edu/a2/text/likes",
        method : "POST",
        // dataType: "application/json",
        data: {"paragraph": paragraph_number},
        success: function(response){
            id = "paragraph_" + paragraph_number;
            like_button = document.getElementById(id).getElementsByTagName("button")[0];
            like_button.innerHTML= "Likes "+ response.data.likes;
        },
        error: function(){
            console.log("Error: API call failed (POST)");
        }
    });
}
