import pytest
import requests

# from time import sleep

# COMPONENT_INDEX_URL = "http://elaster:5000"

# COMPONENT_MONSTER_BASE_URL = COMPONENT_INDEX_URL + '/elaster'



# def test_get_mainpage():
# 	# print('component tester sleeping for 1 sec to let the identidock app to be ready adn also start its server')
# 	# sleep(1)
# 	page = requests.get(COMPONENT_INDEX_URL)
# 	assert page.status_code == 200
# 	assert 'Joe Bloggs' in str(page.text)




# def test_post_mainpage():
# 	page = requests.post(COMPONENT_INDEX_URL, data=dict(name="Moby Dock"))
# 	assert page.status_code == 200
# 	assert 'Moby Dock' in str(page.text)




# def test_mainpage_html_escaping():
# 	page = requests.post(COMPONENT_INDEX_URL, data=dict(name='"><b>TEST</b><!--'))
# 	assert page.status_code == 200
# 	assert '<b>' not in str(page.text)



# def test_get_identicon_with_valid_name_and_invalid_post_method_should_return_405():
# 	name_hash = 'ABCDEF123456789'
	
# 	page = requests.post('{0}/{1}'.format(COMPONENT_MONSTER_BASE_URL, name_hash))
	
# 	assert page.status_code == 405




# def test_get_identicon_with_valid_name_and_cache_miss():	
# 	name_hash = 'ABCDEF123456789AGAIN'
# 	page = requests.get('{0}/{1}'.format(COMPONENT_MONSTER_BASE_URL, name_hash))
	
# 	# print('page.content : {0}'.format(page.content))
# 	assert page.status_code == 200




# def test_get_identicon_with_valid_name_and_cache_hit():	
# 	name_hash = 'ABCDEF123456789AGAIN'
# 	page = requests.get('{0}/{1}'.format(COMPONENT_MONSTER_BASE_URL, name_hash))
	
# 	# print('page.content : {0}'.format(page.content))
# 	assert page.status_code == 200




# def test_get_identicon_with_insecure_and_unescaped_invalid_name_hash():
# 	invalid_name_hash = '<b>;i_am_invalid|name <{"'

# 	page = requests.get('{0}/{1}'.format(COMPONENT_MONSTER_BASE_URL, invalid_name_hash))
	
# 	# print('page.content : {0}'.format(page.content))
# 	assert page.status_code == 200




if __name__ == '__main__':
	# unittest.main()
	pytest.main()
