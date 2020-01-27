## Do not delete or rename any parameters. Only change the default values within quotes if required ##
default_standard_package = ['EST SINGLE TITLE', 'SVOD', 'RENTAL', 'CATCHUP VOD', 'CATCHUP EPISODE', 'SVOD EPISODE', 'DPL SVOD', 'DPL CATCHUP', 'DPL SVOD EPISODE', 'DPL CATCHUP EPISODE']
default_vrp_package = ['VRP SVOD', 'VRP PREMIUM VOD', 'VRP_RENTAL', 'VRP CATCHUP VOD', 'VRP CATCHUP EPISODE', 'VRP SVOD EPISODE', 'VRP DPL SVOD', 'VRP DPL CATCHUP', 'VRP DPL SVOD EPISODE', 'VRP DPL CATCHUP EPISODE']
# Movie File Parameters
video_path = 'Providers/BSS/Content/Distribution/TestFiles/adi_t/'
image_path = 'tank/Images/adi_t/'
hdr_movie_file = 'IdentExternalDDplus_MainWithExternalAtmos_IdentExternalDDplus-Ateme_out_API.ts'
hdr_movie_checksum = 'cb6a578d7551d7908c7ee88c3bdf9deb'
sdr_movie_file = 'CATS_EP1_UHD_3170_1mins.ts'
sdr_movie_checksum = '806761c26916f9a26abb547188c62cf6'
hd_movie_file = 'HD_MOVIE.ts'
hd_movie_checksum = '2e78cb32788e099db6a3118a074bc9a9'
est_movie_file = 'HD_MOVIE.ts'
est_movie_checksum = '2e78cb32788e099db6a3118a074bc9a9'
title_movie = 'SD_2_min.ts'
title_checksum = '8e003a54635310a6da4d7bdff4f96c46'
dpl_movie_url = 'VT-3954178-1-1-THD-CP_001.ts'
dpl_movie_checksum = '2e78cb32788e099db6a3118a074bc9a9'

# Default Metadata Parameters
default_synopsis = 'This is the synopsis of title named: '
default_provider_version = '1'
default_production_year = '2000'
default_ca_btc = 'U'
default_par_rating = '1'
default_audio_type = 'Dolby Digital'
default_frame_rate = '25'
default_subtitle_flag = 'false'
default_asset_runtime = '1:30:00'
default_asset_duration = 'PT1H30M00S'

# EST Show Specific Parameters
tv_show_provider = 'est__tvboxset_hd'
tv_episode_provider = 'est__tvbsepisode_hd'
movie_show_provider = 'est__movieboxset_hd'
movie_episode_provider = 'est__moviebstitle_hd'
default_no_of_seasons = '1'
default_no_of_episodes = '2'

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
trailer_file = 'FinestHours_Trailer.ts'
standard_image_group = ['FinestHours_182x98.jpg', 'FinestHours_182x243.jpg', 'FinestHours_262x349.jpg', 'FinestHours_456x257.jpg']