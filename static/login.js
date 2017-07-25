/*$.ajax({
    url : '../templates/layout.html',
    headers: { 
        'Content-Type': 'application/json'
    },
    crossDomain: true,
    method: 'POST',
    type: 'POST',
    dataType:'json',
    data: JSON.stringify(login),
    success : function(data) { // executes in ajax success
        if(data.success){ //assuming data contains success and message
            alert('Logged in successfully....');
            $(location).attr('href', "/ui/index.html");
        }
        else{
            alert(data.error.msg) // assuming data contains error                       and message
        }
    },
    error : function(data) { // executes only if ajax fails
        alert('Error....');
    }
    }); */

var ajaxRequest;  // The variable that makes Ajax possible!
function ajaxFunction(){
   try{  
      // Opera 8.0+, Firefox, Safari
      ajaxRequest = new XMLHttpRequest();
   }catch (e){
      // Internet Explorer Browsers
      try{
         ajaxRequest = new ActiveXObject("Msxml2.XMLHTTP");
      } catch (e) {
         try{
            ajaxRequest = new ActiveXObject("Microsoft.XMLHTTP");
         } catch (e){
            // Something went wrong
            alert("Your browser broke!");
            return false;
         }
      }
   }
}


function validateAccount(){
    ajaxFunction();
   
   // Here processRequest() is the callback function.
   ajaxRequest.onreadystatechange = processRequest;
   
   if (!target) target = document.getElementById("userid");
   var url = "validate?id=" + escape(target.value);
   
   ajaxRequest.open("GET", url, true);
   ajaxRequest.send(null);
}
