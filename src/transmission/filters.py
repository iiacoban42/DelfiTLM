"""Telemetry filters"""
import django_filters
from django import forms
from .models import Downlink, Uplink, TLE


class TelemetryDownlinkFilter(django_filters.FilterSet):
    """Filter downlink telemetry by frame date interval, frequency and qos ranges"""
    frame_date = django_filters.DateFromToRangeFilter(field_name="timestamp",
                                                      widget=forms.widgets.DateTimeInput(
                                                          attrs={'type': 'datetime-local'}
                                                      )
                                                      )
    frequency = django_filters.RangeFilter(field_name="frequency")

    class Meta:
        """Meta class to specify model"""
        model = Downlink
        fields = ["processed", "invalid", "observer"]


class TelemetryUplinkFilter(django_filters.FilterSet):
    """Filter uplink telemetry by frame date interval, frequency and qos ranges"""
    frame_date = django_filters.DateFromToRangeFilter(field_name="timestamp",
                                                      widget=forms.widgets.DateTimeInput(
                                                          attrs={'type': 'datetime-local'}
                                                      )
                                                      )
    frequency = django_filters.RangeFilter(field_name="frequency")

    class Meta:
        """Meta class to specify model"""
        model = Uplink
        fields = ["processed", "invalid", "operator"]


class TLEFilter(django_filters.FilterSet):
    """Filter TLEs by date and satellite"""
    valid_from = django_filters.DateFromToRangeFilter(field_name="valid_from",
                                                      widget=forms.DateInput(
                                                          attrs={
                                                              'id': 'datepicker',
                                                              'type': 'text'
                                                          }
                                                      ))

    class Meta:
        """Meta class to specify model"""
        model = TLE
        fields = ["sat"]
