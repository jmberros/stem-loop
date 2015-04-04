#!/usr/bin/env ruby
# encoding: utf-8

require 'rubygems'
require 'bundler/setup'

Bundler.require(:default)

require 'fileutils' # Necessary?

include ActionView::Helpers::DateHelper

require_relative './lib/infernal'
require_relative './lib/rfam'
require_relative './lib/calibration_script'
