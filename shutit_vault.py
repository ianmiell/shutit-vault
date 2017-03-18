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
		shutit.send('vault server -dev &')
		shutit.send('export VAULT_ADDR=http://127.0.0.1:8200')
		shutit.send('vault write secret/hello value=world')
		shutit.send('vault write secret/hello value=world excited=yes')
		shutit.send('vault read secret/hello')
		shutit.send('vault read -format=json secret/hello')
		shutit.send('vault read -format=json secret/hello | jq -r .data.excited')
		shutit.send('vault delete secret/hello')
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
