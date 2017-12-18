from shutit_module import ShutItModule

class shutit_vault(ShutItModule):


	def build(self, shutit):
		shutit.install('wget')
		shutit.install('unzip')
		shutit.install('jq')
		shutit.send('wget -qO- https://releases.hashicorp.com/vault/0.7.0/vault_0.7.0_linux_amd64.zip?_ga=1.14381107.503913442.1489821102 > vault.zip')
		shutit.send('unzip vault.zip')
		shutit.send('chmod +x vault')
		shutit.send('mv vault /usr/local/bin')
		shutit.send('vault server -dev > /tmp/vault_out 2>&1 &')
		export_cmd = shutit.send_and_get_output('grep "export VAULT_ADDR" /tmp/vault_out')
		shutit.send(export_cmd)
		unseal_key = shutit.send_and_get_output(r'''grep "Unseal Key:" /tmp/vault_out | sed 's/.*: \(.*\)/\1/' ''')
		root_token = shutit.send_and_get_output(r'''grep "Root Token:" /tmp/vault_out | sed 's/.*: \(.*\)/\1/' ''')
		shutit.send('vault auth ' + root_token)
		# tokens always have a parent, and when that parent token is revoked, children can also be revoked all in one operation. 
		token_output = shutit.send_and_get_output('vault token-create | grep "^token "')
		shutit.send('vault auth ' + token_output)
		shutit.send('vault write secret/hello value=world')
		shutit.send('vault write secret/hello value=world excited=yes')
		shutit.send('vault read secret/hello')
		shutit.send('vault read -format=json secret/hello')
		shutit.send('vault read -format=json secret/hello | jq -r .data.excited')
		shutit.send('vault delete secret/hello')
		shutit.send('vault mount generic')
		shutit.send('vault mounts')
		shutit.send('vault unmount generic')
		shutit.send('vault token-revoke ' + token_output)
		shutit.send('vault auth ' + root_token)
		shutit.send('vault auth-enable github')
		shutit.send('vault write auth/github/config organization=shutit')
		shutit.send('vault write auth/github/map/teams/default value=default')
		# This won't work, as the private token is not used
		shutit.send('#vault auth -method=github token=e6919b17dd654f2b64e67b6369d61cddc0bcc7d5')
		shutit.send('vault auth-disable github')
		shutit.pause_point('')

		return True

def module():
	return shutit_vault(
		'imiell.shutit_vault.shutit_vault', 718123781.0001,
		description='',
		maintainer='',
		delivery_methods=['docker'],
		depends=['shutit.tk.setup']
	)
