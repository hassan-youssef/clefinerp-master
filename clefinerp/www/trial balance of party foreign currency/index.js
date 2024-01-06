frappe.ready(function(){
    generateReport();
    get_company_accounts();  
});
$('#company').on('change' , function(){        
    get_company_accounts();    
});
$('#report').on('click' , function(){        
    generateReport();    
});

$('#export').on('click' , function(){
    exportExcelFile();
});

function get_company_accounts(){
    let company = $('#company').val();
    frappe.call({
        method: "clefinerp.www.trial balance of party foreign currency.index.get_company_accounts",
        args: {'company' :  company},
        callback: function(r) { 
            acccounts = r.message ;
            let html = `<option ></option>`; 
            for(account in acccounts){
                html += `<option >${acccounts[account].name}</option>`
            }
            $('#select_account').html(html);
        }       
    });
}

function generateReport(){
    let company = $('#company').val();
    let from_date = $('#from-date').val();
    let to_date = $('#to-date').val();
    let currency = $('#select_presentation_currency').val();
    let account = $('#select_account').val();
 
    frappe.call({
        method: "clefinerp.www.trial balance of party foreign currency.index.convert_currency",
        args: { 
            'company' :  company ,
            'from_date' : from_date ,
            'to_date' : to_date ,        
            'currency' : currency ,
            'account' : account            
        },
        callback: function(r) {           
            let results = r.message ;             
            if(results == undefined){
                $('#results').html('');
            }else{
                let cur ;                                
                if(!currency && account){
                    cur = `(${results[0].account_currency})` ; 
                }else if(!currency && !account){
                    cur = "" ;
                }else{
                    cur = `(${currency})`; 
                }                           
                let html = `<tr><th></th><th>Customer</th><th>Balance ${cur}</th></tr>`;                
                for(let row in results){                
                    html += `<tr><th class="text-center">${Number(row)+1}</th>
                    <td id="party">${results[row].party}</td>
                    <td id="balance">${format_currency(results[row].balance.balance , ' ' , 3)}</td>
                    </tr>`;
                }
                html += `</table>`;  
                $('#results').html(html);
            }           
                            
        }           
        });
}

function exportExcelFile(){
    let company = $('#company').val();
    let from_date = $('#from-date').val();
    let to_date = $('#to-date').val();
    let currency = $('#select_presentation_currency').val();
    let account = $('#select_account').val();    
  
    window.open(
        "/api/method/clefinerp.www.trial balance of party foreign currency.index.export_as_excel_file?"
        +"company="+encodeURIComponent(company)
        +"&from_date="+encodeURIComponent(from_date)
        +"&to_date="+encodeURIComponent(to_date) 
        +"&currency="+encodeURIComponent(currency)
        +"&account="+encodeURIComponent(account)      
        
    );


}

