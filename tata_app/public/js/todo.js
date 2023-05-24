frappe.ui.form.on('Opportunity', {
	onload(frm) {
		console.log("hello")
	    var element = document.querySelectorAll(".form-section")[7];
		element.classList.add("section-no");
		// your code here
		set_css(frm);
         var user = frappe.session.user_email;

        frappe.call({
			method: "user_number",
			args: { 'user_number': user },
		}).then(records => {
			var num = records["message"];
			console.log(num)
			var agent_number = num	;
			frm.add_custom_button(__('Click-To-Call'), function(){
				var phone=frm.doc.phone;
				var whatsapp_no = frm.doc.whatsapp;
				var phone_ext = frm.doc.phone_ext;
				var destination_number = frm.doc.contact_mobile;
			
				
				if(destination_number==null){
					var destination_number="";
				}
				if(phone_ext==null){
					var phone_ext="";
				}
				if(whatsapp_no==null){
					var whatsapp_no="";
				}
				if(phone==null){
					var phone="";
				}
	
					frappe.confirm(
						"Are you sure want To Call?" + "<br><br>" + "<input type='radio' id='1' name='a' value=" + destination_number + "><label for='html'>"+ "Moblie No :- "+destination_number + "</label><br>" + "<input type='radio' id='2' name='a' value=" + phone + "><label for='html'>"+ "Phone No :- " + phone + "</label><br>"+ "<input type='radio' id='3' name='a' value=" + whatsapp_no + "><label for='html'>"+ "Whats-App No :- " + whatsapp_no + "</label><br>"+ "<input type='radio' id='4' name='a' value=" + phone_ext + "><label for='html'>"+ "Phone Ext No :- " + phone_ext + "</label><br>",
		  
				  function(){
					var a1=document.querySelector('input[name="a"]:checked').value;
						console.log(a1)
						// alert(a1)
						if(a1==""){
							frappe.msgprint("you Don't Have Any Number so you can't connect call",'Error')
						}
						else{
							
							frappe.call({
								
								method:"tata_app.api.click_to_call", 
								args: {'agent_number':agent_number,'destination_number':a1},
								callback: function(r) {
									alert("done")
								}
							});
						}	
					}
					)
	  
			  })
	
	
		})  
	
	},
	
	call3:function(frm){
		var no =frm.doc.phone
		click_call(frm,no)
	},
	call1:function(frm){
		var no =frm.doc.contact_mobile
		click_call(frm,no)
	},
	call2:function(frm){
		var no =frm.doc.whatsapp 
		click_call(frm,no)
	},
	call4:function(frm){
		var no =frm.doc.phone_ext
		click_call(frm,no)
	},
});



function click_call(frm,no){
	if(no==null)
	{
		frappe.msgprint("you Don't Have Phone Number so you can't connect call",'Error')		
    }
	else
	{
		var user = frappe.session.user_email;
			frappe.call({
				method: "user_number",
				args: { 'user_number': user }
			}).then(records => {
				var num = records["message"];
				var agent_number = num	
						frappe.confirm(
							"Are you sure want To Call?",				
						function(){
						frappe.call({
							method:"tata_app.api.click_to_call", 
							args: {'agent_number':agent_number,'destination_number':no},
							callback: function(r) {
							}
						});
						}
						)
					})
		}
}

function connect_to_call(agent_number){
    var a1=document.querySelector('input[name="a"]:checked').value;
						console.log(a1)
						// alert(a1)
						if(a1==""){
							frappe.msgprint("you Don't Have Any Number so you can't connect call",'Error')
						}
						else{
							
							frappe.call({
								
								method:"tata_app.api.click_to_call", 
								args: {'agent_number':agent_number,'destination_number':a1},
								callback: function(r) {
									// alert("done")
								}
							});
						}	
}

function set_css(frm){
	console.log("set_css")
    document.querySelectorAll("[data-fieldname = 'call4']")[1].style.backgroundColor = '#0275d8'
	document.querySelectorAll("[data-fieldname = 'call4']")[1].style.color = '#fff'
	// document.querySelectorAll("[data-fieldname='phone']")[1].style.marginRight ="10px"
	
	document.querySelectorAll("[data-fieldname = 'call1']")[1].style.backgroundColor = '#0275d8'
	document.querySelectorAll("[data-fieldname = 'call1']")[1].style.color = '#fff'
	
	document.querySelectorAll("[data-fieldname = 'call2']")[1].style.backgroundColor = '#0275d8'
	document.querySelectorAll("[data-fieldname = 'call2']")[1].style.color = '#fff'
	
	document.querySelectorAll("[data-fieldname = 'call3']")[1].style.backgroundColor = '#0275d8'
	document.querySelectorAll("[data-fieldname = 'call3']")[1].style.color = '#fff'

	document.querySelectorAll(".section-no .frappe-control")[0].style.marginBottom = '-12px';
	document.querySelectorAll(".section-no .frappe-control")[0].style.width = '75%';
	document.querySelectorAll(".section-no .frappe-control")[1].style.display = 'flex';

	document.querySelectorAll(".section-no .frappe-control")[2].style.marginBottom = '-12px';
	document.querySelectorAll(".section-no .frappe-control")[2].style.width = '75%';
	document.querySelectorAll(".section-no .frappe-control")[3].style.display = 'flex';

	document.querySelectorAll(".section-no .frappe-control")[4].style.marginBottom = '-12px';
	document.querySelectorAll(".section-no .frappe-control")[4].style.width = '75%';
	document.querySelectorAll(".section-no .frappe-control")[5].style.display = 'flex';

	document.querySelectorAll(".section-no .frappe-control")[6].style.marginBottom = '-12px';
	document.querySelectorAll(".section-no .frappe-control")[6].style.width = '75%';
	document.querySelectorAll(".section-no .frappe-control")[7].style.display = 'flex';


	$(".section-no .control-input").css("width","70%")	
	$(".section-no .control-input").css("float","left")	
	$(".section-no .control-input").css("margin-right","10px")	
	console.log("hello end css")
}
