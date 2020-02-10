## Do not delete or rename any parameters. Only change the default values within quotes if required ##
# HTML Server Properties
template_dir = '../templates'
static_dir = '../static'

# Allowed Package Types
default_standard_package = ['EST SINGLE TITLE', 'SVOD', 'RENTAL', 'CATCHUP VOD', 'CATCHUP EPISODE', 'SVOD EPISODE', 'DPL SVOD', 'DPL CATCHUP', 'DPL SVOD EPISODE', 'DPL CATCHUP EPISODE']
default_vrp_package = ['VRP SVOD', 'VRP PREMIUM VOD', 'VRP_RENTAL', 'VRP CATCHUP VOD', 'VRP CATCHUP EPISODE', 'VRP SVOD EPISODE', 'VRP DPL SVOD', 'VRP DPL CATCHUP', 'VRP DPL SVOD EPISODE', 'VRP DPL CATCHUP EPISODE']

# Default Metadata Parameters
default_synopsis = 'This is the synopsis of title named: '
default_provider_version = '1'
default_production_year = '2000'
default_ca_btc = '1'
default_par_rating = '1'
default_audio_type = 'Dolby 5.1'
default_frame_rate = '25'
default_subtitle_flag = 'false'
default_asset_runtime = '1:30:00'
default_asset_duration = 'PT1H30M00S'

# EST Show Specific Parameters
tv_show_provider = 'est__tvboxset_hd'
tv_episode_provider = 'est__tvbsepisode_hd'
movie_show_provider = 'est__movieboxset_hd'
movie_episode_provider = 'est__moviebstitle_hd'
est_title_provider = 'est__sbo_hd'
default_no_of_seasons = '1'
default_no_of_episodes = '2'
uk_std_price = '7.95'
uk_vip_price = '6.95'
il_std_price = '8.95'
il_vip_price = '7.95'

# ADI POST Endpoint Parameters
ts1_cms = 'http://localhost:14231/gateway/submit?'
ts1_vms = 'http://chipdlvwebt01.broadcast.bskyb.com/opencase/ContentProcessor/resource/rest/triggerworkflow?'
ts2_cms = 'http://localhost:14231/gateway/submit?'
ts2_vms = 'http://chipdlvwebt03.broadcast.bskyb.com/opencase/ContentProcessor/resource/rest/triggerworkflow?'
ts3_cms = 'http://localhost:14231/gateway/submit?'
ts3_vms = 'http://10.83.6.7/opencase/ContentProcessor/resource/rest/triggerworkflow?'
ts4_cms = 'http://localhost:14231/gateway/submit?'
ts4_vms = 'http://chipdlvinstt03.broadcast.bskyb.com/opencase/ContentProcessor/resource/rest/triggerworkflow?'
stage_cms = 'http://localhost:14231/gateway/submit?'
stage_vms = 'http://vmswkflowapt01.broadcast.bskyb.com/opencase/ContentProcessor/resource/rest/triggerworkflow?'

# TAR DIRECTORIES
premium_upload_dir = '../supp_files'
premium_vrp_dir = '../created_package'

# TANK CONFIGURATIONS
tank_host = 'chiethstors101.broadcast.bskyb.com'

# OMDB
omdb_host = 'http://www.omdbapi.com/?t='
omdb_api_key = '9534a8be'
omdb_image_dir = '../OMDB_Images/'