#!/usr/bin/env ruby
# encoding: utf-8

#require 'rubygems'
#require 'bundler/setup'
#Bundler.require(:default)

require 'colorize'
require 'mustache'
require 'pry-debugger' if ENV['DEBUG']
# ^ This workaround sucks, I should be using the Gemfile
require 'optparse'

require 'fileutils' # Necessary?

#require 'action_view' # FUCK Nokogiri
#include ActionView::Helpers::DateHelper

APP_ROOT = File.dirname  __FILE__

require_relative './lib/logger'
$logger = Logger.new

require_relative './lib/utils'
$utils = Utils.new

require_relative './lib/infernal'
require_relative './lib/rfam'
require_relative './lib/calibration_manager'
require_relative './lib/utils'
