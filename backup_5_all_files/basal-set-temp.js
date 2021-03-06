'use strict';

function reason(rT, msg) {
  rT.reason = (rT.reason ? rT.reason + '. ' : '') + msg;
  console.error(msg);
}

var tempBasalFunctions = {};

tempBasalFunctions.getMaxSafeBasal = function getMaxSafeBasal(profile) {

    var max_daily_safety_multiplier = (isNaN(profile.max_daily_safety_multiplier) || profile.max_daily_safety_multiplier == null) ? 3 : profile.max_daily_safety_multiplier;
    var current_basal_safety_multiplier = (isNaN(profile.current_basal_safety_multiplier) || profile.current_basal_safety_multiplier == null) ? 4 : profile.current_basal_safety_multiplier;

    return Math.min(profile.max_basal, max_daily_safety_multiplier * profile.max_daily_basal, current_basal_safety_multiplier * profile.current_basal);
};

tempBasalFunctions.setTempBasal = function setTempBasal(rate, duration, profile, rT, currenttemp) {
    //var maxSafeBasal = Math.min(profile.max_basal, 3 * profile.max_daily_basal, 4 * profile.current_basal);

    var maxSafeBasal = tempBasalFunctions.getMaxSafeBasal(profile);
    var round_basal = require('./round-basal');

    if (rate < 0) {
        rate = 0;
    } else if (rate > maxSafeBasal) {
        rate = maxSafeBasal;
    }

    var suggestedRate = round_basal(rate, profile);
    if (typeof(currenttemp) !== 'undefined' && typeof(currenttemp.duration) !== 'undefined' && typeof(currenttemp.rate) !== 'undefined' && currenttemp.duration > (duration-10) && currenttemp.duration <= 120 && suggestedRate <= currenttemp.rate * 1.2 && suggestedRate >= currenttemp.rate * 0.8 && duration > 0 ) {
        rT.reason += " "+currenttemp.duration+"m left and " + currenttemp.rate + " ~ req " + suggestedRate + "U/hr: no temp required";
        rT.rate = currenttemp.rate; //ahmed
        rT.duration = currenttemp.duration-5; //ahmed
	rT.basal = profile.current_basal; //ahmed
	rT.running_temp = currenttemp; //ahmed
	
        return rT;
    }

    if (suggestedRate === profile.current_basal) {
      if (profile.skip_neutral_temps) {
        if (typeof(currenttemp) !== 'undefined' && typeof(currenttemp.duration) !== 'undefined' && currenttemp.duration > 0) {
          reason(rT, 'Suggested rate is same as profile rate, a temp basal is active, canceling current temp');
          //rT.rate = profile.current_basal; //ahmed
          //rT.duration = duration; //ahmed
          rT.duration = 0; //added by default, commented by me
          rT.rate = 0; //added by default, commented by me
		rT.basal = profile.current_basal; //ahmed
		rT.running_temp = currenttemp; //ahmed
          return rT;
        } else {
          reason(rT, 'Suggested rate is same as profile rate, no temp basal is active, doing nothing');
          //rT.rate = profile.current_basal; //ahmed
          //rT.duration = duration-5; //ahmed
		rT.basal = profile.current_basal; //ahmed
		rT.running_temp = currenttemp; //ahmed
          return rT;
        }
      } else {
        reason(rT, 'Setting neutral temp basal of ' + profile.current_basal + 'U/hr');
        rT.duration = duration;
        rT.rate = suggestedRate;
	rT.basal = profile.current_basal; //ahmed
	rT.running_temp = currenttemp; //ahmed
        return rT;
      }
    } else {
      rT.duration = duration;
      rT.rate = suggestedRate;
	rT.basal = profile.current_basal; //ahmed
	rT.running_temp = currenttemp; //ahmed
      return rT;
    }
};

module.exports = tempBasalFunctions;
