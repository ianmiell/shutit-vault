import shutit

vault_version = '0.10.4'
unseal_key = None
root_token = None
token_output = None

s = shutit.create_session(session_type='vagrant', loglevel='debug', echo=True, vagrant_session_name='hashivault', vagrant_memory='2048')

s.login('vagrant ssh')
s.login('sudo su -')

s.install('wget')
s.install('unzip')
s.install('jq')
s.send('wget -qO- https://releases.hashicorp.com/vault/' + vault_version + '/vault_' + vault_version + '_linux_amd64.zip > vault.zip')
s.send('unzip vault.zip')
s.send('chmod +x vault')
s.send('mv vault /usr/local/bin')
s.send('vault -autocomplete-install')
s.send('vault server -dev > /tmp/vault_out 2>&1 &')
s.send(s.send_and_get_output('grep "export VAULT_ADDR" /tmp/vault_out'))

# Get the Vault unseal key and root token
unseal_key = s.send_and_get_output(r'''grep "Unseal Key:" /tmp/vault_out | sed 's/.*: \(.*\)/\1/' ''')
root_token = s.send_and_get_output(r'''grep "Root Token:" /tmp/vault_out | sed 's/.*: \(.*\)/\1/' ''')

s.send('vault auth ' + root_token)

# tokens always have a parent, and when that parent token is revoked, children can also be revoked all in one operation. 
token_output = s.send_and_get_output('vault token-create | grep "^token "')

s.send('vault auth ' + token_output)
s.send('vault write secret/hello value=world')
s.send('vault write secret/hello value=world excited=yes')
s.send('vault read secret/hello')
s.send('vault read -format=json secret/hello')
s.send('vault read -format=json secret/hello | jq -r .data.excited')
s.send('vault delete secret/hello')
s.send('vault mount generic')
s.send('vault mounts')
s.send('vault unmount generic')
s.send('vault token-revoke ' + token_output)
s.send('vault auth ' + root_token)
s.send('vault auth-enable github')
s.send('vault write auth/github/config organization=shutit')
s.send('vault write auth/github/map/teams/default value=default')
# This won't work, as the private token is not used
s.send('#vault auth -method=github token=e6919b17dd654f2b64e67b6369d61cddc0bcc7d5')
s.send('vault auth-disable github')
s.pause_point('')

s.logout()
s.logout()
