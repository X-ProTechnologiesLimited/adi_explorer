from flask import request
class form_input_params(object):
    def __init__(self):
        self.asset_form_input = {}

    def get_form_values(self):
        self.asset_form_input['provider_id'] = request.form.get('provider_id')
        self.asset_form_input['title'] = request.form.get('title')
        self.asset_form_input['service_key'] = request.form.get('service_key')
        self.asset_form_input['multiformat_id'] = request.form.get('multiformat_id')
        self.asset_form_input['svod_season_number'] = request.form.get('svod_season_number')
        self.asset_form_input['svod_episode_number'] = request.form.get('svod_episode_number')
        self.asset_form_input['svod_total_episodes'] = request.form.get('svod_total_episodes')
        self.asset_form_input['dpl_asset_parts'] = request.form.get('dpl_asset_parts')
        self.asset_form_input['order_type'] = request.form.get('order_type')
        self.asset_form_input['po_type'] = request.form.get('po_type')
        self.asset_form_input['est_show_type'] = request.form.get('est_show_type')
        self.asset_form_input['seasons'] = request.form.get('seasons')
        self.asset_form_input['no_of_episodes'] = request.form.get('no_of_episodes')
