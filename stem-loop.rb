#!/usr/bin/env ruby
# encoding: utf-8

require 'rubygems'
require 'bundler/setup'

#Bundler.require(:default)
require 'colorize'
require 'action_view'
require 'mustache'
require 'pry-debugger'
# ^ This workaround sucks

require 'fileutils' # Necessary?

include ActionView::Helpers::DateHelper

APP_ROOT = File.dirname  __FILE__

require_relative './lib/infernal'
require_relative './lib/rfam'
require_relative './lib/calibration_script'
