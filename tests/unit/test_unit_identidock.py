from doubles import allow, expect, ClassDouble, allow_constructor
import pytest
from ci_testing_python.app import identidock



class Mocked_Redis(object):

	def __init__(self):
		self.db = {}

	def get(self, key):
		if key in self.db:
			return self.db[key]
		else:
			return None


	def set(self, key, value):
		self.db[key] = value
		return value




class Mocked_Image(object):

	def __init__(self):
		self.img = 'Mocked_Image'
		self.img_content = b'Mocked_Image_Content'

	@property
	def content(self):
		return self.img_content

	@property
	def value(self):
		return self.img




@pytest.fixture(scope='module')
def mocked_image(request):
	img = Mocked_Image()
	return img


@pytest.fixture(scope='function')
def mocked_redis(request):
	redis = Mocked_Redis()
	return redis


def test_get_mainpage(client):
	page = client.get("/")
	assert page.status_code == 200
	assert 'Joe Bloggs' in str(page.data)




def test_post_mainpage(client):
	page = client.post("/", data=dict(name="Moby Dock"))
	assert page.status_code == 200
	assert 'Moby Dock' in str(page.data)




def test_mainpage_html_escaping(client):
	page = client.post("/", data=dict(name='"><b>TEST</b><!--'))
	assert page.status_code == 200
	assert '<b>' not in str(page.data)




def test_get_identicon_with_valid_name_and_invalid_post_method_should_return_405(client, mocked_image):
	cache = identidock.cache	
	name_hash = 'ABCDEF123456789'
	allow(cache).get.with_args(name_hash).and_return(mocked_image.content)
	
	page = client.post('/monster/{0}'.format(name_hash))
	
	assert page.status_code == 405




def test_get_identicon_with_valid_name_and_cache_hit(client, mocked_image):
	cache = identidock.cache	
	name_hash = 'ABCDEF123456789'
	allow(cache).get.with_args(name_hash).and_return(mocked_image.content)
	
	page = client.get('/monster/{0}'.format(name_hash))
	
	assert page.status_code == 200




def test_get_identicon_with_valid_name_and_cache_miss(client, mocked_redis, mocked_image):
	# cache = ClassDouble(identidock.redis.StrictRedis)
	# allow_constructor(cache).with_args(host='redis', port=6379, db=0).and_return(mocked_redis)

	cache = identidock.cache	
	name_hash = 'ABCDEF123456789'
	allow(cache).get.with_args(name_hash).and_return(None)
	allow(cache).set.with_args(name_hash, mocked_image.content).and_return(mocked_image.content)

	req = identidock.requests
	# expect(req).get
	allow(req).get.and_return(mocked_image)
	# allow(image).content.and_return(image_content)
	
	page = client.get('/monster/{0}'.format(name_hash))
	
	print('Page.Data :  {0}'.format(page.data))
	assert page.status_code == 200




def test_get_identicon_with_insecure_and_unescaped_invalid_name_and_cache_hit(client, mocked_image):
	cache = identidock.cache	
	invalid_name = '<b>;i_am_invalid|name <{"'

	allow(cache).get.and_return(mocked_image.content)
	
	page = client.get('/monster/{0}'.format(invalid_name))
	
	assert page.status_code == 200
	

	
	


if __name__ == '__main__':
	# unittest.main()
	pytest.main()
