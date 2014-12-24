require 'csv'
require 'digest'
require 'erb'
require 'fileutils'
require 'yaml'

require File.join(File.dirname(__FILE__), 'ext/hash_extensions.rb')
require File.join(File.dirname(__FILE__), 'scriptfilter.rb')

# LASTPASS SHELL COMMANDS:
LPASS_COMMAND_LOGIN = 'login'
LPASS_COMMAND_DOWNLOAD = 'export'
LPASS_COMMAND_DETAILS = 'show'

# PASSWORD GENERATION CONSTANTS:
NUM_PASSWORDS = 10         # The number of passwords to generate
DEFAULT_PASSWORD_LEN = 20  # The default length (if no arg is specified)
USE_NUMBERS = true         # Whether the password should include numbers
USE_SYMBOLS = true         # Whether the passwork should include symbols
AVOID_AMBIGUOUS = true     # Whether ambiguous chars should be ignored

LETTERS = [('A'..'Z'), ('a'..'z')]
NUMBERS = (0..9)
AMBIGUOUS_CHARACTERS = %w{ 0 O I l 1 }
SYMBOLS = %w{ ! @ # $ % ^ &amp; * ( ) , . ; : &#039; &quot; / ? \ | ` ~ + = - _ \s }

# MISC. CONSTANTS:
DEFAULT_FILEPATH_CONFIG = File.join(File.expand_path(ENV['HOME']), '.lpvm_config')
DEFAULT_FILEPATH_CACHE = '/tmp/lp_data.csv'
DEFAULT_FILEPATH_LPASS = '/usr/local/bin/lpass'
DEFAULT_SHOULD_CACHE = true

# LastPassVault Class
# The primary object for interating with a LastPass
# vault and its data.
class LastPassVault
  # Stores the preference to cache data.
  # @return [Bool]
  attr_accessor :cache_data

  # Stores the filepath to the cached data.
  # @return [String]
  attr_accessor :cache_data_path

  # Stores the configuration data.
  # @return [Hash]
  attr_accessor :config

  # Stores the filepath to the configuration file
  # @return [String]
  attr_accessor :config_path

  # Stores the filepath to the lpass executable
  # @return [String]
  attr_accessor :lpass_path

  # Initializer.
  # @param [Hash] config A configuration Hash
  # @cache_data_path [String] A filepath to the cached data
  # @return [Void]
  # def initialize(cache = false, cache_data_path = DEFAULT_FILEPATH_CACHE)
  def initialize()
  end

  # Downloads LastPass data for caching purposes.
  # @return [Void]
  def download_data
    FileUtils.rm(@cache_data_path) if File.file?(@cache_data_path)
    File.write(@cache_data_path, `#{ @lpass_path } #{ LPASS_COMMAND_DOWNLOAD }`)
  end

  # Retrieves LastPass data, either from the cache or from
  # LastPass itself if necessary
  # @return [String]
  def get_data
    if @cache_data
      download_data unless File.file?(@cache_data_path)
      data = structify(File.read(@cache_data_path))
    else
      data = structify(`#{ @lpass_path } #{ LPASS_COMMAND_DOWNLOAD }`)
    end
    data
  end

  # Generates a number of random passwords.
  # @param [Integer] number_of_pws The number of passwords to generate
  # @param [Integer] pw_length The length of password to generate
  # @return [Array]
  def generate_passwords(number_of_pws, pw_length)
    # Figure out if the user passed in their own length:
    length = pw_length.nil? || pw_length.empty? ? DEFAULT_PASSWORD_LEN : pw_length.to_i

    # Combine the characters needed based on preferences:
    chars = LETTERS.map { |i| i.to_a }.flatten
    chars.concat(NUMBERS.to_a) if USE_NUMBERS
    chars.concat(SYMBOLS.to_a) if USE_SYMBOLS
    chars = chars - AMBIGUOUS_CHARACTERS if AVOID_AMBIGUOUS

    # Return an array of generated passwords:
    passwords = []
    (1..number_of_pws.to_i).each do |p|
      passwords << (1..length).map { chars[rand(chars.length)] }.join
    end
    passwords
  end

  def get_item_details(item_name)
    # Load the item's info from LastPass:
    info = `#{ @lpass_path } #{ LPASS_COMMAND_DETAILS } #{ item_name }`
    lines = info.split("\n")
    tokens = Hash[lines[1..-1].map do |i|
      pieces = i.partition(': ')
      [pieces[0], pieces[2]]
    end]

    hostname = lines[0].partition(' [')[0]
    hostname_pieces = hostname.partition('/')
    group = hostname_pieces[0]
    name = hostname_pieces[2]

    # Create a new LastPassVaultItem:
    LastPassVaultItem.new(
      tokens.delete('URL'),
      tokens.delete('Username'),
      tokens.delete('Password'),
      hostname,
      name,
      group,
      tokens
    )
  end

  # Loads the configuration Hash from the values in a flat file.
  # @param [String] filepath The configuration filepath
  # @return [Void]
  def load_config(filepath = DEFAULT_FILEPATH_CONFIG)
    # Load the user's config (or create and save if
    # if it doesn't exist):
    if File.file?(DEFAULT_FILEPATH_CONFIG)
      @config = YAML.load(File.read(DEFAULT_FILEPATH_CONFIG))
    else
      @config = {
        filepaths: {
          cache:  DEFAULT_FILEPATH_CACHE,
          config: DEFAULT_FILEPATH_CONFIG,
          lpass:  DEFAULT_FILEPATH_LPASS
        },
        preferences: {
          cache: true
        }
      }
    end

    # Save some specific, useful properties:
    @cache_data = load_property_from_config(:preferences, :cache, DEFAULT_SHOULD_CACHE)
    @cache_data_path = load_property_from_config(:filepaths, :cache, DEFAULT_FILEPATH_CACHE)
    @config_path = load_property_from_config(:filepaths, :config, DEFAULT_FILEPATH_CONFIG)
    @lpass_path = load_property_from_config(:filepaths, :lpass, DEFAULT_FILEPATH_LPASS)

    # Save the configuration data back to the configuration file:
    save_config(filepath)
  end

  # Loads a property from the configuration Hash; if not found,
  # a default is loaded.
  # @param [Symbol] *keys The keys to search for
  # @param [String] default A default value
  # @return [String]
  def load_property_from_config(*keys, default)
    value = @config.dig(*keys)
    value.nil? ? default : value
  end

  # Save the configuration hash to a flat file:
  # @param [String] filepath The configuration filepath
  # @return [Void]
  def save_config(filepath = DEFAULT_FILEPATH_CONFIG)
    File.open(filepath, 'w') { |file| file.write(@config.to_yaml) }
  end

  # Searches the vault for any item who's hostname or URL contains
  # a passed query.
  # @param [String] query The query to search for
  # @return [LastPassVaultItem]
  def search_vault(query)
    vault_data = get_data
    words = query.split(' ')
    vault_data.select { |i| match_all?(i.url, words) || match_all?(i.hostname, words) }
  end

  # LastPassVaultItem Struct
  # A simple struct to manage a LastPass vault entry:
  LastPassVaultItem = Struct.new(:url, :username, :password, :hostname, :name, :grouping, :options) do
    # Turns the struct into a string suitable for a Script Filter arg:
    # @return [Void]
    def to_arg
      CGI.escapeHTML(self.members.map { |m| "#{ m }:#{ self[m] }"}.join('***'))
    end

    # Generates a UID based on the :hostname parameter:
    # @return [String]
    def uid
      Digest::SHA256.hexdigest(self.hostname)
    end
  end

  private

  # Determines whether a string contains portions of a
  # specific Array of words.
  # @param [String] str The string to search
  # @param [Array] words The strings to search for
  # @return [Bool]
  def match_all?(str, words)
    words.all? {|w| str =~ /.*#{ Regexp.quote w }.*/i }
  end

  # Turns CSV data into an Array of LastPassVaultItems.
  # @param [String] csv_data
  # @retun Array
  def structify(csv_data)
    # Create a custom CSV converter to remove empty strings:
    CSV::Converters[:blank_to_nil] = lambda do |field|
      field && field.empty? ? nil : field
    end

    # Create an Array of Hashes that contains all the
    # CSV data:
    results = CSV.new(
      csv_data,
      :headers => true,
      :header_converters => :symbol,
      :converters => [:all, :blank_to_nil]
    ).to_a.map { |row| row.to_hash unless row.empty? }.compact

    # Finally, convert the Array of Hashes into an Array of LastPassVaultItems:
    results.map { |row| LastPassVaultItem.new(*row.values_at(*LastPassVaultItem.members)) }
  end
end

# MAIN SCRIPT:

# Instantiate a LastPassVault:
lpv = LastPassVault.new
lpv.load_config

case ARGV[0]
# Authenticates the user.
# Expected Query: A LastPass username
# Query Optional: ves
when 'authenticate'
  username = ARGV[1]
  if username.nil? || username.empty?
    # username = lpv.config.dig(:authentication, :username)
    username = lpv.load_property_from_config(:authentication, :username, '')
    if username.empty?
      puts "No username found in config file!"
    end
  else
    # Store the passed username in the config file:
    lpv.config.merge!(authentication: { username: username })
    lpv.save_config
  end

# Downloads and caches LastPass data.
# Expected Query: <none>
# Query Optional: N/A
when 'download'
  lpv.download_data
  puts 'LastPass data downloaded!'

# Generates a list of passwords.
# Expected Query: An integer (e.g., 10)
# Query Optional: Yes
when 'generate-password'
  passwords = lpv.generate_passwords(NUM_PASSWORDS, ARGV[1])
  xml = scriptfilter_xml do
    passwords.map do |p|
      scriptfilter_block(p, p, p, 'Click to copy password to the clipboard.')
    end.join.chomp
  end
  puts xml

# Outputs a password from a vault item.
# Expected Query: A LastPassVaultItem arg
# Query Optional: N/A
when 'password'
  password = ARGV[1].split('***').select { |i| i.include?('password') }[0]
  puts password.partition(':')[2]

# Searches the vault for items.
# Expected Query: A string to search for
# Query Optional: No
when 'search-vault'
  results = lpv.search_vault(ARGV[1])
  xml = scriptfilter_xml do
    results.map do |r|
      scriptfilter_block(r.uid, r.to_arg, r[:hostname], r[:username])
    end.join.chomp
  end
  puts xml

# Returns info for a particular vault item.
# Expected Query: A string to search for
# Query Optional: No
when 'show-item'
  puts 'here'
  # hostname = ARGV[1].split('***').select { |i| i.include?('hostname') }[0]
  # puts hostname.partition(':')[2]
  # item = lpv.get_item_details(hostname.partition(':')[2])
  # xml_items = [
  #   { text: 'Open URL in browser', key: :url, action: :open },
  #   { text: 'Copy username to clipboard', key: :username, action: :copy },
  #   { text: 'Copy password to clipboard', key: :password, action: :copy },
  #   { text: 'Copy hostname to clipboard', key: :hostname, action: :copy },
  #   { text: 'Copy name to clipboard', key: :name, action: :copy },
  #   { text: 'Copy group to clipboard', key: :grouping, action: :copy }
  # ]
  #
  # xml = scriptfilter_xml do
  #   xml_items.map do |i|
  #     uid = Digest::SHA256.hexdigest(i[:text] + item[i[:key]])
  #     arg = i[:action].to_s + '***' + item[i[:key]].to_s
  #     scriptfilter_block(uid, arg, i[:text], item[i[:key]])
  #   end.join.chomp
  # end
  # puts xml

# Outputs a username from a vault item.
# Expected Query: A LastPassVaultItem arg
# Query Optional: N/A
when 'username'
  username = ARGV[1].split('***').select { |i| i.include?('username') }[0]
  puts username.partition(':')[2]

# Opens a vault item's URL in the default browser.
# Expected Query: A LastPassVaultItem arg
# Query Optional: N/A
when 'url'
  url = ARGV[1].split('***').select { |i| i.include?('url') }[0]
  `open #{ url.partition(':')[2] }`
end

