from gevent import monkey
monkey.patch_all()
import StringIO
import paramiko
from gittle import Gittle

key_data='-----BEGIN RSA PRIVATE KEY-----\r\nMIIEqAIBAAKCAQEAnr9sGbo5JXs51zwFikdZpxgYvBItXsXpo88NZBirZlAzUF51\r\ncxEykiga+5bor0GgP0lG62uAYw5M/jPrIdpHx+Ge/H4NMAtZ40tB8zR8ifE3Egly\r\nmPCQRDJI9McW+MadqAp+4XdfLMx2slul5k0tlGkZDdD/N8RwKsJW1GZL8vGmqw3n\r\nR1YduMyyAXStJjX8Ptg1zZI5OQzWseltc4ch19m59v1SUkWg0feW97vY3F/tAOZB\r\nILi53vMSNtCV1HXGSctIlq3wIO48qbfWTb1Rm24ZfsoqfB6hX0MRbukYv3NuewiH\r\nfQ/+59tuEdcIOdV5lH38xNA4J8rQhTyiz8rHOwIDAQABAoIBAQCVmLBHIl19+7zL\r\nHq3d3FUZCLUubjbBK+J70r+8xx6mYQeqQgmOMPOmFhMvacvGdCKN4QDrEzg+oJhf\r\nqQ94rFmee/i12heVYe0IK8BvbtO5rk2GOs76XyCkk3p66S61q32ggJuG31YaQmfM\r\ntl8FQ0+jntLUWVJY/E3zjYYDzI7f1epUnQlXNOEF8br0fPZbHdr+H7VVx4TUhIei\r\ncpwkDcdVgyGlxGuvi799HVZ1l2SpFgs2OofuBpgbZKRzYi8pCgGpISMo514xO/Ta\r\naaSLBITEXA/3yqbzzetWo3pu03LbrzH/b1EF05i29NGKxB22jPiQNwwF9TBRe6z1\r\nhdS5iCnZAoIAgQC52Jxmab+CyJmULYF7X1I+KayX5kWLgp/4/sDkRwZl9qI+hIj3\r\nGtr2/c3SMu6Vbfx9TT9wJ0oRRQ4oG1lHf1AlWFx0bYb2PE02MQxHJjH+yyKRidTo\r\nxhvkZDRb4cr+Xz3XIngawUb/bQb8dKwDLWk0NUWmGCR0I9iH8n3R7YiDPQKCAIEA\r\n2qwi9hwoicphYYJKfNlr85aboADJ43ALGRZhMYFjMamvumIcJECCYbuamNr6nDjs\r\n8jXkpQZ0QhVe7W58jB6EdmnRKr6OwwrCc4yggRh1tRukXURBmEBdHTyntufLCi8w\r\nSnadeuSLwm6VOFE8C8X5LjmFh0nqiNL4uBS4rhvTu9cCggCAGB17be6a4yWUiB2/\r\nh3q++UH/G1bN/2RbzbuA3B47Pk/ajbI085uQfixA4N2rB8jV0oyLhsoSWltTkvC5\r\njQWAKNhmZtUvhhQdEMMcjL7wDdfeDHSOJAZQ6Dn4cVPDO26wX5Ihc5dQ1yQWm/un\r\ntmHWHOgsuXi4gjmEh1935B2mcSECggCANxS9Cbk2DN9JgEJNeP1bT9RUBw2rzPpg\r\nEUWt3cZ1sgDIHu6voAIP1YZn/rDKB6ffJ3Oj0F270xmG+8+k17aoLxugcF/nngGL\r\n0YdOtrXukFwSHtwembc8vSyWImBoqHwSce9G47nF6ofoVnM/6MdJaPdcRyO7TBO4\r\nSsYNbu3be6kCggCAalxKvdYqli/HXxPMdyE8yhQxnlNs3p30jeqhSWseyVnVNjbt\r\niKssyM2tF1E+k6VVabf0z3PH0L7TXeyGkNk/rwzhu66sj1an4hSCBDZG+Gm2tjIZ\r\n/Vqglf6owaPxh+aTff5nvb65p9BX3oXQyZUq2mMpNWe6AmPiOHUxLQcUHok=\r\n-----END RSA PRIVATE KEY-----'
key_file = StringIO.StringIO(key_data)
key = paramiko.RSAKey.from_private_key(key_file)

repo_path = '/Users/aaron/git/SEO'
repo_url = 'git@github.com:SamyPesse/ENode.git'

kwargs = {
    'username': 'git',
    'pkey': key,
}

repo = Gittle.clone_remote(repo_url, repo_path, **kwargs)
print(repo.tracked_files)
