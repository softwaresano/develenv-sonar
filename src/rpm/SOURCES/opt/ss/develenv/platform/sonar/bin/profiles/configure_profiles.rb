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

  def deactivate_rule(language, rule_id)
    warn "http://localhost/api/qualityprofiles/search?qualityProfile=CDN&language=#{language}"
    key = response_json("http://localhost/api/qualityprofiles/search?qualityProfile=CDN&language=#{language}",
                        'Get')['profiles'][0]['key']
    response = response_http(
      "http://localhost/api/qualityprofiles/deactivate_rule?key=#{key}&rule=#{rule_id}",
      'Post'
    )
    puts "#{language}:#{rule_id}:#{response.code}"
  end

  def deactivate_rules
    rules_file = File.open('/opt/ss/develenv/platform/sonar/conf/deactivate_rules').read
    rules_file.gsub!(/\r\n?/, "\n")
    rules_file.each_line.reject { |x| x.strip == '' }.join.each_line do |rule_line|
      rule = rule_line.split
      deactivate_rule(rule[0], rule[1])
    end
  end

  def activate_rule(language, rule_id, params)
    warn "http://localhost/api/qualityprofiles/search?qualityProfile=CDN&language=#{language}"
    key = response_json("http://localhost/api/qualityprofiles/search?qualityProfile=CDN&language=#{language}",
                        'Get')['profiles'][0]['key']
    response = response_http(
      "http://localhost/api/qualityprofiles/activate_rule?key=#{key}&rule=#{rule_id}#{params}",
      'Post'
    )
    puts "#{language}:#{rule_id}:#{response.code}"
  end

  def activate_rules
    rules_file = File.open('/opt/ss/develenv/platform/sonar/conf/activate_rules').read
    rules_file.gsub!(/\r\n?/, "\n")
    rules_file.each_line.reject { |x| x.strip == '' }.join.each_line do |rule_line|
      rule = rule_line.split
      rule[2] ||= ''
      activate_rule(rule[0], rule[1], rule[2])
    end
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
pf_loader.activate_rules
pf_loader.deactivate_rules

