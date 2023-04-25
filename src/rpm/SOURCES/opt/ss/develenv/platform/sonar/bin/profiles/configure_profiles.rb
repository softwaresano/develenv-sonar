#!/usr/bin/ruby
# frozen_string_literal: true

require 'net/http'
require 'uri'
require 'json'

# Clone internal sonar profiles and load all rules
class ProfilesLoader
  def initialize
    file_data = File.read('/opt/ss/develenv/platform/sonar/conf/.admin_password').split
    @password = file_data[-1]
    @user = file_data[-3]
  end

  def response_http(url, method = 'Get')
    uri = URI.parse(url)
    request = method == 'Get' ? Net::HTTP::Get.new(uri) : Net::HTTP::Post.new(uri)
    request.basic_auth(@user, @password)

    req_options = {
      use_ssl: uri.scheme == 'https'
    }

    Net::HTTP.start(uri.hostname, uri.port, req_options) do |http|
      http.request(request)
    end
  end

  def response_json(url, method)
    JSON.parse(response_http(url, method).body)
  end

  def clone_profile(source)
    puts ">>> Cloning #{source}"
    quality_profile = 'CDN'
    new_profile = response_json("http://localhost/api/qualityprofiles/copy?fromKey=#{source['key']}&toName=#{quality_profile}",
                                'Post')
    response_json("http://localhost/api/qualityprofiles/activate_rules?targetKey=#{new_profile['key']}&statuses=READY",
                  'Post')
    response_http(
      "http://localhost/api/qualityprofiles/set_default?language=#{new_profile['language']}&qualityProfile=#{quality_profile}",
      'Post'
    )
  end

  def load
    internal_profiles = response_json('http://localhost/api/qualityprofiles/search', 'Get')['profiles'].select do |x|
      x['isBuiltIn'] == true
    end
    internal_profiles.each do |profile|
      clone_profile(profile)
    end
  end
end
pf_loader = ProfilesLoader.new
pf_loader.load
